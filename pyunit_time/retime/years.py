# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/4/14 17:42
# @Author: Jtyoui@qq.com
# @Notes : 处理年份
from pyunit_gof import IObserver
import re


class Years(IObserver):
    def __init__(self):
        self.key = None
        self.time = None
        self.current_year = None
        self.shift_flag = None

    def notify(self, observable, *args, **kwargs):
        self.key = observable.key
        self.time = kwargs['time']
        # self.current_year = observable.current_time.year % 100  # 获取现在年
        self.current_year = observable.current_time.year  # lyc修改点
        self.set_shift_flag()
        self.deal_number_year()
        self.deal_word_year()
        self.set_shift_year()
        return self.time

    def deal_number_year(self):
        """处理带有数字的年,只能匹配2位数字或者四位数字

        比如： 两位数字的年份只能是19年或者2019年
        """
        # match = re.search(r'([12]\d{3}|\d{2})(?=年)', self.key)
        if self.shift_flag:  # xx年前、xx年后 类型的
            return
        match = re.search(r'(\d{1,4})(?=年)', self.key)  # lyc修改点
        if match:
            year = int(match.group())
            if 39 < year < 100:
                year += 1900
            elif 0 <= year <= 30:
                year += 2000
            self.time = self.time.replace(year=year)

    def deal_word_year(self):
        """处理带有文字的年份

        比如：前年、去年等
        """
        word = {
            '大前年': -3,
            '前年': -2,
            '去年': -1,
            '今年': 0,
            '明年': 1,
            '次年': 1,
            '后年': 2,
            '大后年': 3,
        }
        match = re.finditer('|'.join(word.keys()), self.key)
        for m in match:
            self.time = self.time.shift(years=word[m.group()])

    def set_shift_year(self):
        """识别要移动的年份

        比如处理：多少年以后、多少年以前
        """
        if self.shift_flag:
            year = int(self.shift_flag.group())
            year = -year if ('前' in self.key) else year
            self.time = self.time.shift(years=year)

    def set_shift_flag(self):
        """判断是否存在需要移动的年份，设置self.shift_flag

        比如处理：多少年以后、多少年以前
        """
        rule = r'\d+(?=年[以之]?[前后内])|(?<=[前后])\d+(?=年)'
        self.shift_flag = re.search(rule, self.key)
