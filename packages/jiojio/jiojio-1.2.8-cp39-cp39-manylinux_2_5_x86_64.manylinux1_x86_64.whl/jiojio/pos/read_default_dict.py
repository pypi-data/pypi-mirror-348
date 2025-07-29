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
import yaml
from collections import Counter

from jiojio import logging, read_file_by_iter


class ReadPOSDictionary(object):
    """
    由于有大量的词汇，本身仅具有一种词性，故此类词汇无需再进入模型寻找特征，
    直接将词汇映射至最终的词性标签即可，可大量节约计算资源，包括计算耗时、模型参数等。

    - 训练阶段
        - 由于模型最终的 F1 值一般稳定在 91%~95%之间，因此若一个词汇的主词性概率
            大于0.95，则可以将其加入词性词典，例如，
            “手办” 一词在语料中，出现 50 次，其中 49 次都是名词“n”，一次是动词“v”，
            因此，可以将该词直接归入名词词典，训练阶段，不予训练该词。
        - 训练阶段，由于语料的问题，可以优先以该词典的词性为准（进行过数据矫正）
            抽取的特征也应以此为标准；或者，这些词汇的特征不予抽取，节省模型参数量。

    - 推理阶段
        - 同上例，推理阶段可以直接将词典中的词映射至默认标签。

    """
    def __init__(self, config):
        self.default_dict_dir = config.pos_word_dir
        self.pos_types_file = config.pos_types_file
        self.word_pos_dict = dict()
        self.pos_dict_prob = config.pos_dict_prob  # 词典中主词性大于 0.99 的不进入模型训练和预测范围内
        self.pos_dict_freq = config.pos_dict_freq  # 词典中主词性大于该频次的 进行计算，若频次不足则不考虑

        self.pos_type_map = {'nrf': 'nr', 'nr1': 'nr'}  # 将此类词汇词性进行融合
        self._load_word_pos_dict()

    def _load_word_pos_dict(self):
        file_list = os.listdir(self.default_dict_dir)
        for file_name in file_list:
            if not file_name.endswith('.txt'):
                continue

            pos_tag = file_name.split('.')[0]
            pos_tag = self.pos_type_map.get(pos_tag, pos_tag)
            # print(pos_tag)
            # self.pos_word_dict.update({pos_tag: dict()})
            for line in read_file_by_iter(os.path.join(self.default_dict_dir, file_name)):
                if line.count('\t') != 2:
                    continue

                word, prob, freq = line.split('\t')
                prob = float(prob)
                freq = int(freq)
                if prob >= self.pos_dict_prob and freq > self.pos_dict_freq:
                    # 此处应保证一个词汇不同时出现在两个词典中
                    if word in self.word_pos_dict:
                        logging.warn('`{}` exists both in `{}` and `{}`.'.format(
                            word, self.word_pos_dict[word], pos_tag))
                    else:
                        self.word_pos_dict.update({word: pos_tag})
