# -*- coding=utf-8 -*-
# library: jionlp
# author: dongrixinyu
# license: Apache License 2.0
# Email: dongrixinyu.89@163.com
# github: https://github.com/dongrixinyu/Jiojio
# description: Preprocessing tool for Chinese NLP
# Website: http://www.jionlp.com/

"""
DESCRIPTION:
    1、CWS（分词）数据集有两种存储格式
        word 格式，e.g.
            ["他", "指出", "：", "近", "几", "年", "来", "，", "足球场", "风气", "差劲", "。"]
        tag 格式，e.g.
            [['他', '指', '出', '：', '近', '几', '年', '来', '，', '足', '球', '场', '风', '气', '差', '劲', '。'],
             ['B', 'B', 'I', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'I', 'I', 'B', 'I', 'B', 'I', 'B']]

        所有的 CWS 数据均在这两者之间进行转换，为保证数据中 \n\r\t 以及空格等转义
        字符的稳定一致性，均采用 json 格式存储数据。

    2、默认采用的标注标准为 BI 标签格式
        分词有多套标注标准，如 BI、BIES 等等，相差均不大，为了明确词汇边界考虑，
        并减少转移函数错误，默认选择 B(Begin)I(Inside|End)标签标注。

"""

import pdb
from typing import List

from jiojio import logging


__all__ = ['word2tag', 'tag2word']


def _wrong_message(_idx, ts, verbose):
    if verbose:
        logging.info(char_list)
        logging.info(tags)
        logging.warning('wrong tag: {}'.format(
            ts[start if start is not None else max(0, _idx - 2): _idx + 2]))


def word2tag(word_list: List[str]):
    """ 将实体 entity 格式转为 tag 格式，若标注过程中有重叠标注，则会自动将靠后的
    实体忽略、删除。针对单条处理，不支持批量处理。默认采用 BI 标注标准。

    Args:
        word_list(List[str]): 分词词汇的 list
    return:
        List[List[str], List[str]]: tag 格式的数据

    Examples:
        >>> word_list = ["他", "指出", "：", "近", "几", "年", "来", "，", "足球场", "风气", "差劲", "。"]
        >>> print(jio.cws.word2tag(word_list))

        # [['他', '指', '出', '：', '近', '几', '年', '来', '，', '足', '球', '场', '风', '气', '差', '劲', '。'],
        #  ['B', 'B', 'I', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'I', 'I', 'B', 'I', 'B', 'I', 'B']]

    """

    tags = list()
    chars = list()

    for word in word_list:
        word_length = len(word)
        for i in range(word_length):
            if i == 0:
                tags.append('B')
            else:
                tags.append('I')
            chars.append(word[i])

    assert len(chars) == len(tags)
    return [chars, tags]


def tag2word(char_list, tags, verbose=False):
    """ 将 tag 格式转为词汇列表，
    若格式中有破损不满足 BI 标准，则不转换为词汇并支持报错。
    该函数针对单条数据处理，不支持批量处理。
    且仅针对 tag_num 为 2，即 tag 仅有 B 和 I 时的情况。
    Args:
        char_list(str): 输入的文本字符列表
        tags(numpy.ndarray): 文本序列对应的标签
        verbose(bool): 是否打印出抽取实体时的详细错误信息，该函数并不处理报错返回，
            仍按一定形式将有标签逻辑错误数据进行组织并返回。

    Returns:
        list: 词汇列表

    Examples:
        >>> char_list = ['他', '指', '出', '：', '近', '几', '年', '来', '，', '足', '球', '场', '风', '气', '差', '劲', '。']
        >>> char_list = '他指出：近几年来，足球场风气差劲。'
        >>> tags = ['B', 'B', 'I', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'I', 'I', 'B', 'I', 'B', 'I', 'B']
        # for speeding up, `tags` been modified to the following format
        >>> tags = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0]
        >>> print(jio.cws.tag2word(char_list, tags))

        # ["他", "指出", "：", "近", "几", "年", "来", "，", "足球场", "风气", "差劲", "。"]

    """
    chars_length = len(char_list)
    # assert len(char_list) == chars_length, \
    #     'the length of `char list` and `tag list` is not same.'

    word_list = list()
    start = None

    for idx, tag in enumerate(tags):
        # 由于 tag 为 B 的频率高于 tag 为 I，因此首先判断 tag == 0
        if tag == 0:  # tag == 'B'
            if idx == 0:
                start = idx
                if idx == chars_length - 1:  # 即文本中仅一个字
                    word_list.append(char_list)
                    break
                continue

            elif idx != chars_length - 1:
                if start is None:
                    # _wrong_message(idx, tags, verbose)
                    continue
                # if start + 1 == idx:
                #     word = char_list[start]
                # else:
                word_list.append(char_list[start: idx])
                start = idx
            else:  # 即 idx == chars_length - 1
                # if start + 1 == idx:
                #     word_list.append(char_list[start])
                # else:
                word_list.append(char_list[start:idx])
                word_list.append(char_list[-1])

        # elif tag == 1:  # tag == 'I'  # 此步对速度有较大影响，直接改成 else 会加速
        else:
            if idx == 0:
                # _wrong_message(idx, tags, verbose)
                start = idx
                continue
            elif idx != chars_length - 1:
                continue
            else:  # 即 idx == chars_length - 1
                word_list.append(char_list[start:])

        # else:  # 有额外标签，在分词此处默认无
        #     _wrong_message(idx, tags, verbose)
        #     return word_list

        # word_list.append(word)

    # assert len(''.join(word_list)) == chars_length, \
    #     'the length of char list must be same.'
    return word_list
