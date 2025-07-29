# -*- coding=utf-8 -*-
# Library: jiojio
# Author: dongrixinyu
# License: GPL-3.0
# Email: dongrixinyu.89@163.com
# Github: https://github.com/dongrixinyu/jiojio
# Description: fast Chinese Word Segmentation(CWS) and Part of Speech(POS) based on CPU.'
# Website: http://www.jionlp.com/


"""
# 说明：

- 该词典目录包含了各个词性类别所对应的词汇词典
- 词典中的词汇，几乎在任何上下文都属于同一种词性，因此可以直接将其映射为对于词性，
    节省时间，节约模型参数
- 词典中的词汇均包含三部分，词汇、词汇作为主词性出现的概率，词汇作为主词性出现的次数
- 该词典从标注语料中获取，并经过了人工矫正，数据比原语料更准确一些。

"""
