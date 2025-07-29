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
import yaml
import numpy as np

from jiojio import logging, read_file_by_iter


class POSAddDict2Model(object):
    """ 向模型中添加词典，支持用户自定义词典，调节模型，提高模型泛化。
    该方法包含软性和硬性调整两部分。

    词典的构建语法为：<词汇>\t<标签>\t<权重值>
    例如：
        ```
        两面针	nz	0.3
        昆士兰州	ns	0.9
        佩洛西	nr
        ```

    其中定义了三个词汇，`两面针`的词性为专有名词(nz)，`昆士兰州`的词性为地名(ns)，`佩洛西`的词性为人名(nr)。
    1、软性调整部分
        当为词汇指定了权重后，则该词进入软性部分进行权重调整，即，当为词汇计算得到对数化的权重概率后，
        以`两面针`为例：
            [0.002, 0.012, 0.002, -0.001, -0.013, ... 0.349, 0.123, 0.179, 0.001, 0.003]
        该词汇对数化概率值的维度与标签数量一致，假设 nz 对应的概率值为 0.001，即倒数第二项。
        为该项添加权重 0.3，得到：
            [0.002, 0.012, 0.002, -0.001, -0.013, ... 0.349, 0.123, 0.179, 0.301, 0.003]
        这样可以增强 nz 对应的概率权重值。
        软性调整的部分适用于该词汇的词性不确定的时候，例如：“都”包含两个词性，分别表示副词和名词“都城”之意，
        此时，添加软性调整较为合适。

    2、硬性调整部分
        当词汇不指定权重时，则该词进入硬性部分进行权重调整，即直接将词汇映射至标准词性。
        词汇将被添加至词汇表，和工具包默认的`词汇-词性词典`进行融合。

        当词汇的词性具有极强的唯一性时，例如“纽约”，仅指地名，绝无其它含义，则硬性词典映射效率非常高。

    """
    def __init__(self, user_dict_path=None, pos_types_file=None):
        if user_dict_path is None:
            self.soft_word_pos_obj = None
            self.hard_word_pos_obj = None

        else:
            assert type(user_dict_path) is str
            self._add_dict(user_dict_path)

            if pos_types_file is None:
                with open(os.path.join(os.path.dirname(
                              os.path.abspath(__file__)), 'pos_types.yml'),
                          'r', encoding='utf-8') as f:
                    self.pos_types = yaml.load(f, Loader=yaml.SafeLoader)
            self.tag_to_idx = dict(
                [(t, i) for i, t in enumerate(sorted(list(self.pos_types['model_type'].keys())))])

    def _add_dict(self, user_dict_path):

        self.soft_word_pos_obj = dict()
        self.hard_word_pos_obj = dict()

        for idx, line in enumerate(read_file_by_iter(user_dict_path)):
            if line.count('\t') == 2:
                word, pos, weight = line.strip().split('\t')
                weight = float(weight)
                self.soft_word_pos_obj.update({word: [pos, weight]})

            elif line.count('\t') == 1:
                word, pos = line.strip().split('\t')
                self.hard_word_pos_obj.update({word: pos})
            else:
                logging.warning('this line `{}` is illegal.'.format(line))

        if len(self.soft_word_pos_obj) == 0:
            self.soft_word_pos_obj = None

        logging.info('add {} words to pos_user_dict.'.format(idx + 1))

    def __call__(self, word, node_state):
        """为节点状态添加词汇权重，软性增强词汇被识别的能力

        Args:
            word(str): 待处理词汇
            node_state(np.ndarray): 根据模型得到的 numpy 格式的节点状态矩阵

        Returns:
            (numpy.Array): 根据模型增强后的矩阵，该类型无需返回值

        """
        if word in self.soft_word_pos_obj:

            pos_type, weight = self.soft_word_pos_obj[word]
            node_state[self.tag_to_idx[pos_type]] += weight
