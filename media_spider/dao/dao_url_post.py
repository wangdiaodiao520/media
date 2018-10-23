#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import json
import logging
import urllib
import urllib2

from media_spider.util.consts import api_url_mapping

__author__ = 'zengyang@tv365.net(ZengYang)'


def post_item(item):
    logging.info('start write api')
    for key in item:
        if key == 'account':
            continue
        logging.info('%s pages lenth is %s' % (key, len(item[key])))
        url = api_url_mapping[key]
        for single_page in item[key]:
            logging.info('return pages %s===>single_page is %s' % ( key, single_page))
            # head_dict = {'ContentType': 'application/json'}
            # data = urllib.urlencode(single_page)
            # req = urllib2.Request(url=url, data=data, headers=head_dict)
            # res = urllib2.urlopen(req)
            # res = res.read()
            # logging.info('return api msg is %s,pages %s===>single_page is %s' % (res, key, single_page))