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
import json


class Config(object):
    # model_urls = {
    #     "pos": "https://github.com/dongrixinyu/jiojio/releases/download/v1.0.1/pos.zip",
    # }

    def __init__(self):
        # 若自行训练模型，请务必保留该页参数，尤其是特征参数 features params 选取部分，将直接影响结果

        # dirs
        self.jiojio_home = os.path.expanduser('~/.jiojio')
        self.train_dir = os.path.join(self.jiojio_home, 'pos_train_dir')
        self.model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                      'models/default_pos_model')

        # POS 类型文件
        self.pos_types_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'pos_types.yml')
        # 默认词典文件，用于做词汇-词性的直接映射
        self.pos_word_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'dictionary')
        self.pos_dict_prob = 0.99  # 词典中主词性大于 0.99 的不进入模型训练和预测范围内
        self.pos_dict_freq = 0  # 词典中主词性大于该频次的 进行计算，若频次不足则不考虑

        # training params
        self.build_train_temp_files = True  # 重新构建训练语料，否则加载旧语料
        self.process_num = 40
        self.initial_learning_rate = 0.0065  # 梯度初始值
        self.dropping_rate = 0.6  # 维持学习速率，越大则下降越快(0~1) 推荐(0.7~0.999)
        self.random_init = True  # False for 0-init of model weights, True for random init of model weights
        self.train_epoch = 5  # 训练迭代次数
        self.mini_batch = 80000  # mini-batch in stochastic training
        self.nThread = 10  # number of processes in testing and training
        self.regularization = True  # 建议保持
        self.sample_ratio = 0.03  # 抽取总数据集中做训练中途验证的数据集比例
        self.interval = 50  # 按多少间隔 batch 打印日志

        self.feature_train_file = os.path.join(self.train_dir, 'feature_train.txt')
        self.gold_train_file = os.path.join(self.train_dir, 'gold_train.txt')
        self.feature_test_file = os.path.join(self.train_dir, 'feature_test.txt')
        self.gold_test_file = os.path.join(self.train_dir, 'gold_test.txt')

        # features params
        self.norm_text = True  # 将所有的 数字、字母正规化，但该参数基本上是必选参数，否则造成特征稀疏与 F1 值降低
        self.convert_num_letter = True  # 将所有数字、字母、空格等转换为 ascii 形式
        self.normalize_num_letter = False  # 将所有数字正规化为 7，字母正规化为 Z
        self.convert_exception = True  # 将所有异常字符全部转为固定常见字符 ん

        self.char_feature_trim = 68  # 普通字符的频次删减数值 (50/5)
        self.part_length_trim = 4  # part 词缀长度的最大值，超过此值删除，一般固定不变

        # 词缀特征出现次数，该特征数应当小于 unigram_feature_trim 以便把低频的特征抽取出
        # 但是发现有相当多的冗余特征，实际上 part 特征应当有足够的泛性，
        # 如“陕汽通家”，这个词汇，被找出了 “陕汽通” 和 “气通家” 两词，是不正确的特征，
        # 该特征过于特性，无泛性，如 “新远网”、“流光网” 的 “网” 字作为 part 特征
        # 此处需要用到新词发现，找出 part 特征
        self.part_feature_chinese_trim = 300
        self.part_feature_num_trim = 400
        self.part_feature_non_chinese_trim = 1000  # 词缀特征出现次数，低于该值的频次被删除，此为应对英文等字符情况
        self.feature_trim = 68  # 普通特征的删减数值 (60/3)  依然可以继续提高，用以减少特征数量

        # 可以考虑增至 78，用来控制参数数量
        #训练样本数量为 9600000 条。37.69% 的词汇样本进行了模型训练
        # 当 feature_trim = 68 时，特征数
        # 2022-08-02 17:48:21 INFO build: # orig feature num: 24741032
        # 2022-08-02 17:48:35 INFO build: # 86.20% features are saved.
        # 2022-08-02 17:48:35 INFO build: # true feature_num: 53 万个参数

        # 当 feature_trim = 60 时，特征数
        # 2022-08-02 17:48:21 INFO build: # orig feature num: 24741032
        # 2022-08-02 17:48:35 INFO build: # 86.80% features are saved.
        # 2022-08-02 17:48:35 INFO build: # true feature_num: 591176

        # 当 feature_trim = 40 时，特征数
        # 2022-08-01 18:23:51 INFO build: # orig feature num: 25626208
        # 2022-08-01 18:24:06 INFO build: # 88.19% features are saved.
        # 2022-08-01 18:24:06 INFO build: # true feature_num: 835654
        # 因此特征数的 trim 值可以继续提高，用以压缩模型参数的大小。

        self.unigram_feature_trim = 68  # 单词特征的数量 (50/4)
        self.word_max = 4  # 越大，则计算耗时越长，因此不建议超过 6，过短如 3 则会造成模型效果下降

        if False:
            self.interval = 5  # 按多少间隔打印日志
            self.initial_learning_rate = 0.5  # 梯度初始值
            # self.bi_ratio_times = int(1 / self.initial_learning_rate)
            self.dropping_rate = 0.3  # 维持学习速率，越大则下降越快(0~1) 推荐(0.7~0.999)
            self.train_epoch = 4  # 训练迭代次数

            self.char_feature_trim = 15
            self.part_length_trim = 4  # part 词缀长度的最大值，超过此值删除，一般固定不变
            self.part_feature_trim = 30
            self.part_feature_num_trim = 70
            self.part_feature_non_chinese_trim = 50  # 词缀特征出现次数，低于该值的频次被删除，此为应对英文等字符情况
            self.feature_trim = 10
            self.unigram_feature_trim = 5
            self.sample_ratio = 0.3  # 抽取总数据集中做训练中途验证的数据集比例

    def params_check(self):
        assert self.initial_learning_rate > 0
        assert self.train_epoch > 0
        assert self.mini_batch > 0
        # assert self.part_feature_trim < self.part_feature_non_chinese_trim

    def to_json(self):
        # 将关键推理参数，导出为 json 数据，存入模型目录下
        inference_dict = {
            'word_max': self.word_max,
            'norm_text': self.norm_text,
            # 'pos_types_file' : self.pos_types_file,
            'convert_num_letter': self.convert_num_letter,
            'normalize_num_letter': self.normalize_num_letter,
            'convert_exception': self.convert_exception,
        }
        with open(os.path.join(self.model_dir, 'params.json'), 'w', encoding='utf-8') as fw:
            json.dump(inference_dict, fw, ensure_ascii=False, indent=4, separators=(',', ':'))


pos_config = Config()
pos_config.params_check()
