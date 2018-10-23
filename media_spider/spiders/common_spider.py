#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import copy
import logging

import time
import traceback

from scrapy import Request
from scrapy.spiders import CrawlSpider

from media_spider.items import CommonItem
from media_spider.util.consts import source_settings, all_pages

__author__ = 'zengyang@tv365.net(ZengYang)'


class CommonSpider(CrawlSpider):

    def init_common_parser(self, account):
        item = CommonItem()
        item['account'] = account
        for key in source_settings[self._source_name]['pages']:
            self._single_item[key] = copy.deepcopy(all_pages[key])
            if key != 'content_page':
                self._single_item[key]['date'] = time.strftime("%Y%m%d", time.localtime(time.time()))
            self._single_item[key]['data']['platformId'] = account['platformId']
            item[key + 's'] = []
        return item

    def start_requests(self):
        url = source_settings[self._source_name]['login_url']
        items = []
        accounts = source_settings[self._source_name][self._account]
        for index in range(len(accounts)):
            account = accounts[index]
            item = self.init_common_parser(account)
            items.append(item)

        for item in items:
            logging.info('spider account %s start' % item['account']['user_name'])
            yield Request(url, meta={'cookiejar': index, 'account': item['account'], 'item': item},
                          callback=self.after_login, dont_filter=True)

    def x_path(self, response, rule):
        try:
            result = response.xpath(rule).extract()
        except:
            traceback.print_exc()
            logging.error('rule xpath perhaps wrong %s' % rule)
        return result