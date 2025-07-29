# -*- coding=utf-8 -*-
# Library: jiojio
# Author: dongrixinyu
# License: GPL-3.0
# Email: dongrixinyu.89@163.com
# Github: https://github.com/dongrixinyu/jiojio
# Description: fast Chinese Word Segmentation(CWS) and Part of Speech(POS) based on CPU.'
# Website: http://www.jionlp.com/


import os
import pdb
import sys
import json
import ctypes

import numpy as np

from jiojio.pre_processor import PreProcessor
from jiojio.inference import get_log_Y_YY
from jiojio.model import Model
from jiojio import Extractor

from . import cws_tag2word_c, \
    cws_prediction_lib
from .config import Config
from .tag_words_converter import tag2word
from .feature_extractor import CWSFeatureExtractor
from .add_dict_to_model import CWSAddDict2Model


class CWSPredictText(object):
    """ 预测文本，用于对外暴露接口 """
    def __init__(self, model_dir=None, user_dict=None, rule_extractor=False):
        """初始化函数，加载模型及用户词典"""
        default_model_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')

        # 采用规则将某些内容抽取出
        if rule_extractor:
            self.rule_extractor = Extractor()
        else:
            self.rule_extractor = None

        # 指定分词模型目录
        if model_dir is None:
            model_dir = os.path.join(default_model_dir, 'default_cws_model')
        else:
            if os.path.isabs(model_dir):
                pass
            else:
                model_dir = os.path.join(default_model_dir, model_dir)

        self.user_dict = CWSAddDict2Model(user_dict)

        # 加载推理参数
        with open(os.path.join(model_dir, 'params.json'), 'r', encoding='utf-8') as fr:
            config = json.load(fr)

        cws_config = Config()
        for key, val in config.items():
            if hasattr(cws_config, key):
                setattr(cws_config, key, val)

        self.feature_extractor = CWSFeatureExtractor.load(
            config=cws_config, model_dir=model_dir)
        self.model = Model.load(model_dir, task='cws')
        # self.model = Model.load(model_dir, task=None)  # 与 cws 指定有区别

        self.idx_to_tag = {
            idx: tag for tag, idx in self.feature_extractor.tag_to_idx.items()}
        self.tag_num = len(self.idx_to_tag)

        self.pre_processor = PreProcessor(
            convert_num_letter=cws_config.convert_num_letter,
            normalize_num_letter=cws_config.normalize_num_letter,
            convert_exception=cws_config.convert_exception)

        self._prepare_C_func()

    def _prepare_C_func(self):
        # C 方式调用
        self.tag2word_c = cws_tag2word_c

        self.cws_prediction_handle = ctypes.c_void_p(None)

        if cws_prediction_lib is not None:
            cws_prediction_lib.init.argtypes = [
                ctypes.c_int, ctypes.py_object,
                ctypes.c_int, ctypes.py_object,
                ctypes.c_int, ctypes.py_object,
                ctypes.py_object, ctypes.c_int]

            cws_prediction_lib.init.restype = ctypes.c_void_p
            cws_prediction_lib.cut.restype = ctypes.py_object

            unigram_list = list(self.feature_extractor.unigram)
            bigram_list = list(self.feature_extractor.bigram)
            feature_to_idx_list = list(self.feature_extractor.feature_to_idx.keys())
            model_weight_list = self.model.node_weight.tolist()

            # initialization of new_cws_prediction
            self.cws_prediction_handle = ctypes.c_void_p(
                cws_prediction_lib.init(
                    70000, unigram_list,
                    120000, bigram_list,
                    2000000, feature_to_idx_list,
                    model_weight_list,
                    0))  # 1 means to print init process log, 0 means not

            del unigram_list
            del bigram_list
            del feature_to_idx_list
            del model_weight_list

        if (cws_prediction_lib is not None) and (self.tag2word_c is not None):
            self.C_flag = True

            # save memory alloc
            self.model = None
            self.feature_extractor = None

        else:
            self.C_flag = False

    def _cut_C(self, text):
        # old method:

        # length = len(text)
        # all_features = []

        # # the score for every node
        # for idx in range(length):

        #     node_features = self.get_node_features_c(
        #         idx, text, length, self.feature_extractor.unigram,
        #         self.feature_extractor.bigram)

        #     node_feature_idx = self.cws_feature2idx_c(
        #         node_features, self.feature_extractor.feature_to_idx)

        #     all_features.append(node_feature_idx)

        # Y = get_log_Y_YY(all_features, self.model.node_weight, dtype=np.float16)

        # new method:
        Y = cws_prediction_lib.cut(self.cws_prediction_handle, text)
        # print('pure C: ', _Y)
        # print('pipe C: ', Y)

        # add dictionary
        if self.user_dict.trie_tree_obj is not None:
            self.user_dict(text, Y)

        tags_idx = Y.argmax(axis=1).astype(np.int8)

        # print(tags_idx)
        # pdb.set_trace()
        return tags_idx

    def _cut_py(self, text):
        length = len(text)
        all_features = []

        for idx in range(length):

            node_features = self.feature_extractor.get_node_features(idx, text)

            # 此处考虑，通用未匹配特征 “/”，即索引为 0 的特征
            node_feature_idx = [
                self.feature_extractor.feature_to_idx[node_feature]
                for node_feature in node_features
                if node_feature in self.feature_extractor.feature_to_idx]

            if len(node_feature_idx) != len(node_features):
                node_feature_idx.append(0)

            all_features.append(node_feature_idx)

        Y = get_log_Y_YY(all_features, self.model.node_weight, dtype=np.float16)

        # 添加词典
        if self.user_dict.trie_tree_obj is not None:
            self.user_dict(text, Y)

        tags_idx = Y.argmax(axis=1).astype(np.int8)

        # print(tags_idx)
        # pdb.set_trace()
        return tags_idx

    def _cut_with_rule(self, text, with_type=True):
        """采用规则抽取出某些词汇，如ip地址，email，身份证号，url，电话号码等等

        start_flag: 指示正则抽取部分是从 text 的第一个字符就开始的
        end_flag: 指示正则抽取部分是从 text 的最后一个字符结束的

        """
        rule_res_list = self.rule_extractor.extract_info(text, with_type=with_type)

        if len(rule_res_list) == 0:
            # 空匹配
            return [text], [], False, False

        start_flag = False
        end_flag = False

        _rule_res_list = sorted(rule_res_list, key=lambda item: item['o'][0])

        # 将错误的信息进行过滤，连续两个正则抽取部分有重叠
        rule_res_list = [_rule_res_list[0]]
        for item in _rule_res_list[1:]:
            if item['o'][0] < rule_res_list[-1]['o'][1]:
                continue
            rule_res_list.append(item)

        rule_res_length = len(rule_res_list)

        if rule_res_length == 1:
            # 单独处理仅一个正则匹配的情况，用以节省处理时间
            seg_list = []
            item = rule_res_list[0]['o']
            if item[0] != 0:
                seg_list.append(text[: item[0]])
            else:
                start_flag = True

            if item[1] != len(text):
                seg_list.append(text[item[1]:])
            else:
                end_flag = True

            return seg_list, rule_res_list, start_flag, end_flag

        seg_list = []
        for idx in range(rule_res_length):
            item = rule_res_list[idx]['o']
            if idx == 0:
                if item[0] != 0:
                    seg_list.append(text[: item[0]])
                else:
                    start_flag = True

                next_item = rule_res_list[idx + 1]['o']
                seg_list.append(text[item[1]: next_item[0]])

            elif idx == rule_res_length - 1:
                if item[1] != len(text):
                    seg_list.append(text[item[1]:])
                else:
                    end_flag = True

            else:
                next_item = rule_res_list[idx + 1]['o']
                seg_list.append(text[item[1]: next_item[0]])

        return seg_list, rule_res_list, start_flag, end_flag

    def cut(self, text):

        if not text:
            return []

        if self.rule_extractor:
            seg_list, rule_res_list, start_flag, end_flag = self._cut_with_rule(
                text, with_type=False)

            seg_res_list = []
            for segment in seg_list:

                norm_segment = self.pre_processor(segment)
                if self.C_flag:
                    tags = self._cut_C(norm_segment)
                    words_list = self.tag2word_c(
                        segment, tags.ctypes.data_as(ctypes.c_void_p), len(tags))
                else:
                    tags = self._cut_py(norm_segment)
                    words_list = tag2word(segment, tags)

                seg_res_list.append(words_list)

            # 将正则和模型处理的部分进行合并
            words_list = []

            if start_flag:
                for idx in range(len(seg_res_list)):
                    words_list.append(rule_res_list[idx]['s'])
                    words_list.extend(seg_res_list[idx])

                if end_flag:
                    words_list.append(rule_res_list[-1])

            else:
                # pdb.set_trace()
                for idx in range(len(rule_res_list)):
                    words_list.extend(seg_res_list[idx])
                    words_list.append(rule_res_list[idx]['s'])

                if not end_flag:
                    words_list.extend(seg_res_list[-1])

            return words_list

        else:
            # 不进行分片切分的结果
            norm_text = self.pre_processor(text)
            if self.C_flag:
                tags = self._cut_C(norm_text)
                words_list = self.tag2word_c(
                    text, tags.ctypes.data_as(ctypes.c_void_p), len(tags))
            else:
                tags = self._cut_py(norm_text)
                words_list = tag2word(text, tags)

            return words_list

    def cut_with_pos(self, text):
        """ 当后续要接 POS 任务时，需要返回两个 words_list """
        if not text:
            return []

        if self.rule_extractor:
            seg_list, rule_res_list, start_flag, end_flag = self._cut_with_rule(
                text, with_type=True)

            seg_res_list = []
            norm_seg_res_list = []
            for segment in seg_list:

                norm_segment = self.pre_processor(segment)
                if self.C_flag:
                    tags = self._cut_C(norm_segment)
                    tags_length = len(tags)

                    words_list = self.tag2word_c(
                        segment, tags.ctypes.data_as(ctypes.c_void_p), tags_length)
                    norm_words_list = self.tag2word_c(
                        norm_segment, tags.ctypes.data_as(ctypes.c_void_p), tags_length)

                else:
                    tags = self._cut_py(norm_segment)

                    words_list = tag2word(segment, tags)
                    norm_words_list = tag2word(norm_segment, tags)

                seg_res_list.append(words_list)
                norm_seg_res_list.append(norm_words_list)

            words_list = []
            norm_words_list = []

            if start_flag:
                for idx in range(len(seg_res_list)):
                    words_list.append(rule_res_list[idx]['s'])
                    words_list.extend(seg_res_list[idx])

                    norm_words_list.append(rule_res_list[idx]['s'])
                    norm_words_list.extend(norm_seg_res_list[idx])

                if end_flag:
                    words_list.append(rule_res_list[-1]['s'])
                    norm_words_list.append(rule_res_list[-1]['s'])

            else:
                for idx in range(len(rule_res_list)):
                    words_list.extend(seg_res_list[idx])
                    words_list.append(rule_res_list[idx]['s'])

                    norm_words_list.extend(norm_seg_res_list[idx])
                    norm_words_list.append(rule_res_list[idx]['s'])

                if not end_flag:
                    words_list.extend(seg_res_list[-1])
                    norm_words_list.extend(norm_seg_res_list[-1])

            if len(rule_res_list) == 0:  # 为了避免一遍循环
                word_pos_map = None

            else:
                word_pos_map = dict()
                for item in rule_res_list:
                    word_pos_map.update({item['s']: item['t']})

            return words_list, norm_words_list, word_pos_map

        else:
            norm_text = self.pre_processor(text)
            if self.C_flag:
                tags = self._cut_C(norm_text)
                tags_length = len(tags)

                words_list = self.tag2word_c(
                    text, tags.ctypes.data_as(ctypes.c_void_p), tags_length)
                norm_words_list = self.tag2word_c(
                    norm_text, tags.ctypes.data_as(ctypes.c_void_p), tags_length)

            else:
                tags = self._cut_py(norm_text)

                words_list = tag2word(text, tags)
                norm_words_list = tag2word(norm_text, tags)

            return words_list, norm_words_list, None
