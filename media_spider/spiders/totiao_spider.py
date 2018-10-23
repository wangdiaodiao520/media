#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import copy
import datetime
import logging
import time

from scrapy import Request
from scrapy.spiders import CrawlSpider

from media_spider.items import CommonItem
from media_spider.util.basic_type_converter import from_string_to_json
from media_spider.util.consts import all_pages, source_settings


class ToTiaoSpider(CrawlSpider):
    name = 'totiao_spider'
    _platformId = None
    _accountId = None
    _account_name = None
    _pwd = None
    _dt = None
    _COOKIE_QI_E = None
    _source_name = 'toutiao'
    _item = None
    _single_item = {}

    def init_common_parser(self):
        for key in source_settings[self._source_name]['pages']:
            self._single_item[key] = copy.deepcopy(all_pages[key])
            self._single_item[key]['date'] = self._dt
            self._single_item[key]['data']['platformId'] = self._platformId
            self._single_item[key]['data']['accountId'] = self._accountId
            self._item[key + 's'] = []

    def switch_account(self):
        account = qq_kandian_account.pop()
        self._platformId = account['platformId']
        self._accountId = account['accountId']
        self._account_name = account['user_name']
        self._pwd = account['pwd']
        self._COOKIE_QI_E = {}
        self._dt = time.strftime("%Y%m%d", time.localtime(time.time()))
        self._item = CommonItem()

    def start_requests(self):
        if len(qi_e_account) == 0:
            logging.debug('========>no account,spider finish')
            return
        self.switch_account()
        self.init_common_parser()
        logging.debug('========>spider account %s start' % self._account_name)
        url = source_settings[self._source_name]['login_url']
        yield Request(url, meta={'cookiejar': '1', 'user_name': self._account_name, 'pwd': self._pwd},
                      callback=self.parse_index_pages)
        yield Request(url, callback=self.start_requests)

    def parse_index_pages(self, response):
        index_count = response.xpath("//div[@class='notice_set clearfix']/div[2]//p/text()").extract()[0].encode(
            'utf-8')
        fans_count = response.xpath("//div[@class='notice_set clearfix']/div[3]//p/text()").extract()[0].encode('utf-8')
        readCount = response.xpath("//div[@class='notice_set clearfix']/div[4]//p/text()").extract()[0].encode('utf-8')
        # todo:视频播放量
        play_count = response.xpath("//div[@class='notice_set clearfix']/div[5]//p/text()").extract()[0].encode('utf-8')
        index_pages = [
            {'radia': index_count, 'fanCount': fans_count, 'readCount': readCount, 'play_count': play_count}]
        for each_index_page in index_pages:
            self._single_item['index_page']['data']['radia'] = each_index_page['radia']
            self._single_item['index_page']['data']['fanCount'] = each_index_page['fanCount']
            self._single_item['index_page']['data']['readCount'] = each_index_page['readCount']
            self._single_item['index_page']['data']['play_count'] = each_index_page['play_count']
            self._item['index_pages'].append(self._single_item['index_page'])
        now_time = datetime.datetime.now()
        end_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        begin_time = (now_time + datetime.timedelta(days=-31)).strftime('%Y-%m-%d')
        url = 'https://kandian.mp.qq.com/api/analysis_fans/fans_growth?isCompare=0&sDate=%s&eDate=%s' \
              '&compareStartDate=2018-06-25&compareEndDate=2018-07-01&sortOrder=0&type=2' % (
                  self._COOKIE_QI_E[u'userid'], begin_time, end_time)

        yield Request(url, cookies=self._COOKIE_QI_E, callback=self.parse_user_pages)

    def parse_user_pages(self, response):
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        user_pages = dict_result['mainChart']['mainChart']
        for each_user_page in user_pages[:1]:
            self._single_item['user_page']['data']['logtime'] = each_user_page['sendDate'].strftime('%Y-%m-%d')
            self._single_item['user_page']['data']['totalCount'] = each_user_page['data'][0]['totalFollowCount']
            self._single_item['user_page']['data']['getCount'] = each_user_page['data'][0]['newFollowCount']
            self._single_item['user_page']['data']['gdCount'] = each_user_page['data'][0]['addedFollowCount']
            self._single_item['user_page']['data']['loseCount'] = each_user_page['data'][0]['unfollowCount']
            self._item['user_pages'].append(self._single_item['user_page'])
        now_time = datetime.datetime.now()
        end_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        begin_time = (now_time + datetime.timedelta(days=-31)).strftime('%Y-%m-%d')
        # todo:系统升级
        url = 'https://om.qq.com/income/GetUserIncomeList?from=%s&to=%s&relogin=1' % (begin_time, end_time)
        yield Request(url, cookies=self._COOKIE_QI_E, callback=self.parse_income_pages)

    def parse_income_pages(self, response):
        #todo:系统升级
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        incomes = dict_result['data']
        for each_income in incomes:
            self._single_item['income_page']['data']['logtime'] = each_income['date'].replace('-', '')
            self._single_item['income_page']['data']['income'] = each_income['total_amount']
            self._single_item['income_page']['data']['allowance'] = each_income['total_platform_amount']
            self._item['income_pages'].append(self._single_item['income_page'])
        end_time = str(time.time())[:10]
        page_num = 1
        url = 'https://kandian.mp.qq.com/api/analysis_article/get-single-list?current=1&every=15&start_date=2018-07-02&end_date=2018-07-08&token=1256206092' % (
            page_num, end_time)
        yield Request(url, cookies=self._COOKIE_QI_E,
                      meta={'page_num': page_num}, callback=self.parse_content_pages_article)

    def parse_content_pages_article(self, response):
        # todo:系统升级
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        content_pages = dict_result['data']['statistic']
        tota_page = dict_result['data']['totalPage']
        page_num = response.meta['page_num']
        if page_num > int(tota_page):
            return
        for each_content in content_pages:
            self._single_item['content_page']['data']['logtime'] = each_content['pubTime'][:len('2018-01-01')].replace(
                '-', '')
            self._single_item['content_page']['data']['type'] = 1
            self._single_item['content_page']['data']['title'] = each_content['title']
            self._single_item['content_page']['data']['readCount'] = each_content['read']
            self._single_item['content_page']['data']['collectCount'] = each_content['exposure']
            self._single_item['content_page']['data']['dailies'] = []
            articleId = each_content['articleId']
            begin_time = str(time.time() - 24 * 60 * 60 * 8)[:10]
            end_time = str(time.time() - 24 * 60 * 60 * 1)[:10]
            url = 'https://om.qq.com/statistic/ArticleAnalyze?media=%s&article=%s&channel=0&' \
                  'fields=title,read,exposure,relay,collect,postil,updating,comment,read_uv,vv&titleType=0&btime=%s&etime=%s&' \
                  'page=1&num=1000&merge=0&relogin=1' % (
                      self._COOKIE_QI_E[u'userid'], articleId, begin_time, end_time)
            yield Request(url, cookies=self._COOKIE_QI_E, callback=self.parse_content_pages_detail_article)
            self._item['content_pages'].append(self._single_item['content_page'])

        end_time = str(time.time())[:10]
        page_num += 1
        url = 'https://om.qq.com/statistic/ArticleReal?page=%s&num=8&btime=1420041600&etime=%s&relogin=1' % (
            page_num, end_time)
        yield Request(url, cookies=self._COOKIE_QI_E,
                      meta={'page_num': page_num}, callback=self.parse_content_pages_article)
        yield self._item

    def parse_content_pages_detail_article(self, response):
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        content_pages = dict_result['data']['statistic']
        for single_content_page in content_pages:
            single_content_page_dict = {}
            single_content_page_dict['logtime'] = single_content_page['statistic_date'].replace('-', '')
            single_content_page_dict['readCount'] = single_content_page['read']
            single_content_page_dict['pvCount'] = single_content_page['exposure']
            single_content_page_dict['shareCount'] = single_content_page['relay']
            single_content_page_dict['collectCount'] = single_content_page['collect']
            self._single_item['content_page']['data']['dailies'].append(single_content_page_dict)
