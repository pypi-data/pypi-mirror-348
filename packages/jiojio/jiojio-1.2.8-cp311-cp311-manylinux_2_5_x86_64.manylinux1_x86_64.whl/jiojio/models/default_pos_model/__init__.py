# -*- coding=utf-8 -*-
# Library: jiojio
# Author: dongrixinyu
# License: GPL-3.0
# Email: dongrixinyu.89@163.com
# Github: https://github.com/dongrixinyu/jiojio
# Description: fast Chinese Word Segmentation(CWS) and Part of Speech(POS) based on CPU.'
# Website: http://www.jionlp.com


# 2022-08-04
# 该模型训练样本数 960,0000 条，测试样本数 100,0000 条
# 37.70% 的词汇经过了模型，剩余词汇直接由词典映射得到
# 模型参数共 53 万个。
# 模型训练的 acc 值为
#     训练集：token_acc=87.99%  sample_acc=33.81%
#     测试集：token_acc=87.90%  sample_acc=33.60%
# 词典 trim 概率值为 0.99，粗略平均而得 0.995
# 模型 综合 准确率值为
#     0.995 * (1 - 0.3770) + 0.8795 * 0.3770 = 95.14%
