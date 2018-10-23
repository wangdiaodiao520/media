#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import json
import urllib


__author__ = 'zengyang@tv365.net(ZengYang)'
import urllib2


def test1():
    # url = 'http://pre-online.17getfun.com/api/weMedia/indexDataForCrawl'
    url = 'http://pre-online.17getfun.com/api/weMedia/contentDataForCrawlNew'
    item_index_page = {
        'readCount': 2222, 'title': '测试测试', 'platformId': 0, 'logtime': 20180101, 'accountId': 0,
        'dailies': [{'readUser': 30, 'logtime': 20180101}, {'readUser': 303, 'logtime': 20180102}]
    }
    head_dict = {'ContentType': 'application/json'}
    data = urllib.urlencode(item_index_page)
    req = urllib2.Request(url=url, data=data, headers=head_dict)
    res = urllib2.urlopen(req)
    res = res.read()
    pass


def test2():
    # url = 'http://www.tuling123.com/openapi/api'
    # json_data = {"key": "4b6ce82fbe554a11b99dabfa3a4ae6d9", "info": "哈哈", "userid": "jxn"}
    # r = requests.post(url, json=json_data)
    # print(r.text)
    url = 'http://pre-online.17getfun.com/api/weMedia/contentDataForCrawlNew'
    item_index_page = {
        'date': 20180101,
        'data': {
            'readCount': 2222,
            'title': '哈哈',
            'platformId': 0,
            'logtime': 20180101,
            'accountId': 0,
            'dailies': [{'readUser': 30, 'logtime': 20180101}, {'readUser': 303, 'logtime': 20180102}]}
    }
    head_dict = {'ContentType': 'application/json'}
    data = urllib.urlencode(item_index_page)
    data = data.encode()
    req = urllib2.Request(url=url, data=data, headers=head_dict)
    res = urllib2.urlopen(req)
    res = res.read()
    pass


def test3():
    url = "http://pre-online.17getfun.com/api/weMedia/contentDataForCrawlNew"

    head_dict = {'ContentType': 'application/x-www-form-urlencoded'}
    data = 'date=20180101&data=%7B%27readCount%27%3A+2222%2C+%27title%27%3A+%27%E6%B5%8B%E8%AF%95%E6%B5%8B%E8%AF%95%27%2C+%27platformId%27%3A+0%2C+%2C+%27logtime%27%3A+20180101%2C+%27accountId%27%3A+0%2C+%27dailies%27%3A+%5B%7B%27readUser%27%3A+30%2C+%27logtime%27%3A+20180101%7D%2C+%7B%27readUser%27%3A+303%2C+%27logtime%27%3A+20180102%7D%5D%7D'
    req = urllib2.Request(url=url, data=data, headers=head_dict)
    res = urllib2.urlopen(req)
    res = res.read()
    print(res)



