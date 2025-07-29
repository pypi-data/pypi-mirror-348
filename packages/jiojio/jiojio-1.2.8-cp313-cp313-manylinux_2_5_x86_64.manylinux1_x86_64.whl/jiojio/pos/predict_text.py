# -*- coding=utf-8 -*-
# Library: jiojio
# Author: dongrixinyu
# License: GPL-3.0
# Email: dongrixinyu.89@163.com
# Github: https://github.com/dongrixinyu/jiojio
# Description: fast Chinese Word Segmentation(CWS) and Part of Speech(POS) based on CPU.'
# Website: http://www.jionlp.com


import os
import pdb
import sys
import json
import ctypes
import numpy as np

from jiojio.pre_processor import PreProcessor
from jiojio.inference import get_log_Y_YY, viterbi
from jiojio.model import Model

from .config import Config
from .feature_extractor import POSFeatureExtractor
from .add_dict_to_model import POSAddDict2Model
from .read_default_dict import ReadPOSDictionary
from . import get_pos_node_feature_c


class POSPredictText(object):
    """ 预测文本，用于对外暴露接口 """
    def __init__(self, model_dir=None, user_dict=None,
                 pos_rule_types=True):
        """初始化函数，加载模型及用户词典"""
        default_model_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')

        # 指定 POS 模型目录
        if model_dir is None:
            model_dir = os.path.join(default_model_dir, 'default_pos_model')

        else:
            if os.path.isabs(model_dir):
                pass
            else:
                model_dir = os.path.join(default_model_dir, model_dir)

        # 加载推理参数
        with open(os.path.join(model_dir, 'params.json'), 'r', encoding='utf-8') as fr:
            config = json.load(fr)

        pos_config = Config()
        for key, val in config.items():
            if hasattr(pos_config, key):
                setattr(pos_config, key, val)

        if user_dict is not None:
            self.user_dict = POSAddDict2Model(user_dict)
            hard_word_pos_obj = self.user_dict.hard_word_pos_obj
            soft_word_pos_obj = self.user_dict.soft_word_pos_obj
            if soft_word_pos_obj is None:
                self.user_dict = None

        else:
            self.user_dict = None
            hard_word_pos_obj = dict()

        # 加载 default word pos dict
        self.word_pos_default_dict = ReadPOSDictionary(pos_config).word_pos_dict
        for word, pos in hard_word_pos_obj.items():
            if word in self.word_pos_default_dict:
                self.word_pos_default_dict[word] = pos
            else:
                self.word_pos_default_dict.update({word: pos})
        # pdb.set_trace()
        self.pos_rule_types = pos_rule_types

        self.feature_extractor = POSFeatureExtractor.load(
            config=pos_config, model_dir=model_dir)

        self.dtype = np.float16  # 原因在于模型不需要太高精度就可以做区分，此值不需要变
        self.model = Model.load(model_dir, dtype=self.dtype)
        self.node_weight = self.model.node_weight

        self.idx_to_tag = {
            idx: tag for tag, idx in self.feature_extractor.tag_to_idx.items()}
        self.tag_num = len(self.idx_to_tag)

        self.pre_processor = PreProcessor(
            convert_num_letter=pos_config.convert_num_letter,
            normalize_num_letter=pos_config.normalize_num_letter,
            convert_exception=pos_config.convert_exception)

        # C 方式调用
        self.get_pos_node_feature_c = get_pos_node_feature_c

    def _cut(self, words):
        """模型预测部分改为两条线并行

            1、一条线首先考察词汇是否为唯一词性，存在于默认的词汇表中，若存在，直接映射，不经过模型
        根据统计，此类词汇总数占到总词汇的 62%。

            2、另一条线则进入模型进行判断，由此，由于词汇的前后顺序，并非每个词都具有词性分布，
        因此无法进行 viterbi 算法。
        viterbi 算法的效用体现在，形容词后大概率跟着名词和代词，副词常出现在动词之前，等等诸如此类。
        然而在中文文本这种比较松散的分析语中，此种启发式软性规则很难体现在 viterbi 的转移参数中，
        有大量的反例证实上述启发式软性规则在实际具体文本中存在错误。
        此外，viterbi 算法是相当耗时的，尤其是当词性种类多达 20 多种的情况下。放弃 viterbi 可极大
        提升处理速度。对于一个基于 CPU 的词性标注工具，处理速度是极为重要的。

        """
        _part = self.feature_extractor.part
        _unigram = self.feature_extractor.unigram
        _char = self.feature_extractor.char

        length = len(words)
        tags_list = []

        for idx in range(length):

            if words[idx] in self.word_pos_default_dict:
                tags_list.append(self.word_pos_default_dict[words[idx]])

            else:
                if self.get_pos_node_feature_c is None:
                    # 以 python 方式计算，效率较低
                    node_features = self.feature_extractor.get_node_features(idx, words)
                else:
                    # 以 C 方式计算，效率高
                    node_features = self.get_pos_node_feature_c(
                        idx, words, _part, _unigram, _char)

                    # if node_features != self.feature_extractor.get_node_features(idx, words):
                    #     print('C: ', node_features)
                    #     print('py:', self.feature_extractor.get_node_features(idx, words))
                    #     pdb.set_trace()

                node_feature_idx = [
                    self.feature_extractor.feature_to_idx[node_feature]
                    for node_feature in node_features
                    if node_feature in self.feature_extractor.feature_to_idx]
                if len(node_feature_idx) < len(node_features):  # 补充空特征
                    node_feature_idx.append(0)

                Y = np.sum(self.node_weight[node_feature_idx], axis=0)

                # 添加词典
                if self.user_dict is not None:
                    self.user_dict(words[idx], Y)

                tag = self.idx_to_tag[Y.argmax(axis=0)]
                tags_list.append(tag)

        return tags_list

    def cut(self, word_list, word_pos_map=None):

        tags_list = self._cut(word_list)

        if word_pos_map is None:
            return tags_list

        else:
            for idx in range(len(word_list)):
                if word_list[idx] in word_pos_map:
                    tags_list[idx] = word_pos_map[word_list[idx]]

            return tags_list
