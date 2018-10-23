#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

__author__ = 'zengyang@tv365.net(ZengYang)'

yidian_conf = {
    'index_page': {
        'fanCount': "//div[@class='orderDatas']//span[@class='total']/text()",
        'readCount': "//div[@class='clickDatas']//span[@class='total']/text()",
        'pvCount': "//div[@class='viewDatas']//span[@class='total']/text()",
    }
}

qi_e_conf = {
    'index_page': {
        'radia': "//ul[@class='totals-list totals-list-homepage clearfix banner-show']/li/a/span/text()",
    }
}

qq_kandian_conf = {
    'index_page': {
        'radia': "//div[@class='notice_set clearfix']/div[2]//p/text()",
        'fanCount': "//div[@class='notice_set clearfix']/div[3]//p/text()",
        'readCount': "//div[@class='notice_set clearfix']/div[4]//p/text()",
        'play_count': "//div[@class='notice_set clearfix']/div[5]//p/text()"
    }
}
