#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import logging
import urllib2

__author__ = 'zengyang@tv365.net(ZengYang)'


def get_cookie(url):
    try:
        req = urllib2.Request(url)
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153'
        req.add_header("User-Agent", ua)
        f = urllib2.urlopen(req)
        value = f.headers.dict['set-cookie']
        start = value.find('bid=')
        end = value.find(';', start)
        return value[start: end]
    except Exception as e:
        logging.error("****** Failed to get cookie")
    return ''