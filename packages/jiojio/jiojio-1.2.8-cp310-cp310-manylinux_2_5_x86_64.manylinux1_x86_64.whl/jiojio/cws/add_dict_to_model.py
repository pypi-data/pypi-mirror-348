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
import numpy as np

from jiojio import logging, read_file_by_iter, TrieTree

"""
两种利用词典对模型进行加速的方法
一、固定词汇的分词方法唯一性
    有些词汇，在文本中仅具有唯一的分词方式，例如：“邓小平”，不论出现在何种语境中，
    分词方法都只能划分为 “邓小平”，同样的特性也出现在较长的专有名词、如 “阿莫西林”，
    成语、如 “一夫当关”，标点符号、如 “，。？！” 等。
    还有一些词汇，“踌躇”、“徜徉”等，是这些汉字的独有词汇，即其中的汉字，除了组该词外
    几乎不再组其它词汇。因此这些词汇也属于固定词汇类型。
    这些词汇可以制作词典，进行词汇匹配，被匹配的词汇的序列标注标签是固定的，不再经过
    模型。
    具体词典位于 dictionary/cws/default_cws_dictionary.txt

    1、根据统计，某些标点符号如 “-”、“：”难以加入上述词典，原因在于一些反例
        “2019-02-12”、“19：32分” 等。
    2、根据文本统计，此类具有固定分类方法的词汇，大约占总词数的 17%。因此，将这些
        词汇经过模型处理，则可以有效解决一部分问题。使用的词典匹配方法为 trie 树。
        但是由于实现上存在一些问题，导致计算速度反而比未加词典还慢，需要进一步提升。

二、字符本身仅存在一种标签类型
    标签类型在分词中包括 B 和 I。
    某些汉字几乎仅存在一种分词标签，如 “衅” 仅用来组词 “寻衅”、“挑衅”，因此该字可以
    直接匹配标签 I。此外还有词汇有相反的标签，“这”则具有极强的 B 标签特性，“擅”、“垃”
    等字同理。
    将此类字符制作成词典，匹配到即打标，不经过模型，可以加速处理速度。

    1、根据语料统计，当设定一个字符 99% 概率出现在某个标签上时，即将该字符添加在词典
        得到的结果为，大约占总文本字符量 9.9% 的数量的字符会不经过模型由此打标。
    2、实际上，过于频繁的字符，如“这”，其在 B 和 I 标签的出现频率分别为 4803951, 1426
        即，尽管直接将其打为 B 标签而不经过模型，可以达到 99.8%的准确率，但是，仍有
        1426 次的文本中，它并非 B 标签。且这个频次极高，有 bigram 特征可以匹配并且有效

        因此，该种特征实际效果存疑，仍需验证。

所有的词典匹配方法，从某种角度而言，都牺牲了模型特征的独特性，在以一个默认的较大概率进行
直接的匹配，会伤害一部分的特征。

"""


class CWSAddDict2Model(object):
    """ 向模型中添加词典，提高模型泛化
    """
    def __init__(self, user_dict_path=None):
        if user_dict_path is None:
            self.trie_tree_obj = None
        elif user_dict_path is True:
            self.trie_tree_obj = TrieTree()
        else:
            assert type(user_dict_path) is str
            self._add_dict(user_dict_path)

    def _add_dict(self, user_dict_path):

        self.trie_tree_obj = TrieTree()
        for idx, line in enumerate(read_file_by_iter(user_dict_path)):
            if line.count('\t') == 1:
                word, weight = line.strip().split('\t')
                weight = float(weight)
            elif line.count('\t') == 0:
                word = line.strip()
                weight = 1
            else:
                logging.warning('`{}` is illegal.'.format(line))

            self.trie_tree_obj.add_node(word.lower(), weight)  # 要先预处理 TODO

        logging.info('add {} words to `cws_user_dict`.'.format(idx + 1))

        if self.trie_tree_obj.depth > 5:
            logging.warning(
                'the max_depth of trie tree is {}, high max_depth will slow down'\
                ' processing speed. removing long word is advised.'.format(
                    self.trie_tree_obj.depth))

    def __call__(self, text, node_states):
        """为节点状态添加词汇权重，软性增强词汇被识别的能力

        Args:
            text(str): 待处理文本
            node_states: 根据模型得到的numpy 格式的节点状态矩阵

        Returns:
            (numpy.Array): 根据模型增强后的矩阵，该类型无需返回值

        """
        text_length = len(text)
        i = 0

        while i < text_length:
            pointer = text[i: self.trie_tree_obj.depth + i]
            # pointer = pointer_orig.lower()  # 不需要，因预处理已处理过 TODO
            step, val = self.trie_tree_obj.search(pointer)
            if val is not None:
                node_states[i, 0] += val
                node_states[i + 1: i + step, 1] += val

                if i + step < text_length:
                    node_states[i + step, 0] += val

            i += step
