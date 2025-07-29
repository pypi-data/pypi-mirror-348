# -*- coding=utf-8 -*-
# Library: jiojio
# Author: dongrixinyu
# License: GPL-3.0
# Email: dongrixinyu.89@163.com
# Github: https://github.com/dongrixinyu/jiojio
# Description: fast Chinese Word Segmentation(CWS) and Part of Speech(POS) based on CPU.'
# Website: http://www.jionlp.com/


import os
import re
import pdb


__all__ = ['Extractor']


class Extractor(object):
    """ 规则抽取器 """
    def __init__(self):
        self.email_pattern = re.compile(
            r'(?<=[^0-9a-zA-Z.\-])' \
            r'([a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+(?:\.[a-zA-Z0-9_.-]+)*\.[a-zA-Z0-9]{2,6})' \
            r'(?=[^0-9a-zA-Z.\-])')

        self.url_pattern = re.compile(
            r'(?<=[^.])((?:(?:https?|ftp|file)://|(?<![a-zA-Z\-\.])www\.)' \
            r'[\-A-Za-z0-9\+&@\(\)#/%\?=\~_|!:\,\.\;]+[\-A-Za-z0-9\+&@#/%=\~_\|])' \
            r'(?=[<\u4E00-\u9FA5￥，。；！？、“”‘’>（）—《》…● \t\n])')

        ip_single = r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)'
        self.ip_address_pattern = re.compile(
            ''.join([r'(?<=[^0-9])(', ip_single, r'\.', ip_single, r'\.',
                     ip_single, r'\.', ip_single, ')(?=[^0-9])']))

        self.id_card_pattern = re.compile(
            r'(?<=[^0-9a-zA-Z])' \
            r'((1[1-5]|2[1-3]|3[1-7]|4[1-6]|5[0-4]|6[1-5]|71|81|82|91)' \
            r'(0[0-9]|1[0-9]|2[0-9]|3[0-4]|4[0-3]|5[1-3]|90)' \
            r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-3]|5[1-7]|6[1-4]|7[1-4]|8[1-7])' \
            r'(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])' \
            r'\d{3}[0-9xX])' \
            r'(?=[^0-9a-zA-Z])')

        self.cell_phone_pattern = re.compile(
            r'(?<=[^\d])(((\+86)?([- ])?)?((1[3-9][0-9]))([- ])?\d{4}([- ])?\d{4})(?=[^\d])')
        self.landline_phone_pattern = re.compile(
            r'(?<=[^\d])(([\(（])?0\d{2,3}[\)） —-]{1,2}\d{7,8}|\d{3,4}[ -]\d{3,4}[ -]\d{4})(?=[^\d])')

    @staticmethod
    def _extract_base(pattern, text, typing, with_type=True):
        """ 正则抽取器的基础函数

        Args:
            pattern(re.compile): 正则表达式对象
            text(str): 字符串文本
            type(str): 抽取的字段类型

        Returns:
            list: 返回结果

        """
        # `s` is short for text string,
        # `o` is short for offset
        # `t` is short for type
        if with_type:
            return [{'s': item.group(1),
                     'o': (item.span()[0] - 1, item.span()[1] - 1),
                     't': typing}
                    for item in pattern.finditer(text)]
        else:
            return [{'s': item.group(1),
                     'o': (item.span()[0] - 1, item.span()[1] - 1)}
                    for item in pattern.finditer(text)]

    def extract_email(self, text, with_type=True):
        """ 提取文本中的 E-mail

        Args:
            text(str): 字符串文本

        Returns:
            list: email列表

        """
        return self._extract_base(
            self.email_pattern, text, typing='email', with_type=with_type)

    def extract_id_card(self, text, with_type=True):
        """ 提取文本中的 ID 身份证号

        Args:
            text(str): 字符串文本

        Returns:
            list: 身份证信息列表

        """
        return self._extract_base(
            self.id_card_pattern, text, typing='id', with_type=with_type)

    def extract_ip_address(self, text, with_type=True):
        """ 提取文本中的 IP 地址

        Args:
            text(str): 字符串文本

        Returns:
            list: IP 地址列表

        """
        return self._extract_base(
            self.ip_address_pattern, text, typing='ip', with_type=with_type)

    def extract_phone_number(self, text, with_type=True):
        """从文本中抽取出电话号码

        Args:
            text(str): 字符串文本

        Returns:
            list: 电话号码列表

        """
        cell_results = self._extract_base(
            self.cell_phone_pattern, text, typing='tel', with_type=with_type)
        landline_results = self._extract_base(
            self.landline_phone_pattern, text, typing='tel', with_type=with_type)

        return cell_results + landline_results

    def extract_url(self, text, with_type=True):
        """提取文本中的url链接

        Args:
            text(str): 字符串文本

        Returns:
            list: url列表

        """
        return self._extract_base(
            self.url_pattern, text, typing='url', with_type=with_type)

    def extract_info(self, text, with_type=True):
        text = ''.join(['￥', text, '￥'])  # 因 # 可能出现在 url 中

        results_list = list()

        results_list.extend(self._extract_base(self.url_pattern, text, typing='url', with_type=with_type))
        results_list.extend(self._extract_base(self.email_pattern, text, typing='email', with_type=with_type))
        results_list.extend(self._extract_base(self.id_card_pattern, text, typing='id', with_type=with_type))
        results_list.extend(self._extract_base(self.ip_address_pattern, text, typing='ip', with_type=with_type))
        results_list.extend(self.extract_phone_number(text, with_type=with_type))

        return results_list
