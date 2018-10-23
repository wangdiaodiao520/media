#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import time


__author__ = 'zengyang@tv365.net(ZengYang)'


def convert_url(url):
    if url.startswith('/'):
        return 'https://kandian.mp.qq.com' + url
    return url


def convert_time():
    begin_time = str(time.time() - 24 * 60 * 60)[:10]
    end_time = str(time.time())[:10]
    return begin_time, end_time


def replace_common():
    pass


def convert_str(str):
    return -2 if str == '-' or '计算中' in str else str


def convert_str_content(str):
    return -2 if str == '-' else str


def time_stamp_to_time_format(format_str, time_stamp):
    """

    :param format_str: %Y--%m--%d %H:%M:%S
    :param time_stamp: 1381419600
    :return:
    """
    return time.strftime(format_str, time.localtime(time_stamp))


