#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import time


__author__ = 'zengyang@tv365.net(ZengYang)'


def get_time_format(format_str=False, days_compare=0, begining_day_time=False, check_time_stamp=False):
    """
    :param time_stamp: now_time stamp
    :param format_str: exampl~'%Y--%m--%d'，"%Y--%m--%d %H:%M:%S"
    :param days_compare:2 days ago~-2, 2 days later 2
    :param begining_day_time:True 00:00:00 False this time_stamp
    :param check_time_stamp:time_stamp param to convert
    :return:
    """
    time_stamp = time.time()
    if check_time_stamp:
        time_stamp = check_time_stamp
    time_format = time_stamp + days_compare * 24 * 60 * 60
    if format_str:
        timeArray = time.localtime(time_format)
        time_format = time.strftime(format_str, timeArray)
    if begining_day_time:
        time_tmp = get_time_format('%Y-%m-%d', check_time_stamp=time_format)
        time_tmp = time_tmp + ' 00:00:00'
        timeArray = time.strptime(time_tmp, '%Y-%m-%d %H:%M:%S')
        time_format = int(time.mktime(timeArray))
    return time_format


def get_time_stamp_13():
    time_stamp_13 = int(round(time.time() * 1000))
    return time_stamp_13


if __name__ == '__main__':
    time_stamp = time.time()
    # now_time = get_time_format(time_stamp, "%Y%m%d", 0)
    aa = get_time_format(begining_day_time=True)
    bb = get_time_format(days_compare=-2)
    bigin_date = get_time_format(days_compare=-8, begining_day_time=True)
    end_date = get_time_format(days_compare=-2, begining_day_time=True)
    pass
