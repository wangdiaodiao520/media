#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import copy
import datetime
import logging
import time
import traceback

from scrapy import Request

from media_spider.conf.all_spider_conf import yidian_conf
from media_spider.spiders.common_spider import CommonSpider
from media_spider.tools.phantom_js_driver import SeleniumDirverFactory
from media_spider.util.basic_type_converter import from_string_to_json
from media_spider.util.consts import source_settings
from media_spider.util.convert_util import convert_str, time_stamp_to_time_format


class YiDianSpider(CommonSpider):
    name = 'yidian_spider'
    _source_name = 'yidian'
    _account = 'yidian_account'
    _platformId = None
    _dt = None
    _single_item = {}

    def after_login(self, response):
        """
        it's parse_index_pages
        :param response:
        :return:
        """
        item = response.meta['item']
        cookie = response.meta['cookie']
        try:
            pvCount = self.x_path(response, yidian_conf['index_page']['pvCount'])[0].encode('utf-8').replace(',', '')
            fanCount = self.x_path(response, yidian_conf['index_page']['fanCount'])[0].encode('utf-8').replace(',', '')
            readCount = self.x_path(response, yidian_conf['index_page']['readCount'])[0].encode('utf-8').replace(',', '')
            index_pages = [{'fanCount': fanCount, 'readCount': readCount, 'pvCount': pvCount}]
        except:
            traceback.print_exc()
            logging.error('login failed or site templet is out-of-date')
        for each_index_page in index_pages:
            index_page = copy.deepcopy(self._single_item['index_page'])
            index_page['data']['logtime'] = int(index_page['date'])
            index_page['data']['fanCount'] = int(each_index_page['fanCount'])
            index_page['data']['readCount'] = int(float(each_index_page['readCount']))
            index_page['data']['pvCount'] = int(float(each_index_page['pvCount']))
            index_page['data']['accountId'] = item['account']['accountId']
            item['index_pages'].append(index_page)
        now_time = datetime.datetime.now()
        end_time = now_time.strftime('%Y%m')
        url = 'https://mp.yidianzixun.com/api/stat_writer?endMonth=%s' % end_time
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie,
                      callback=self.parse_index_pages_radia, dont_filter=True)

    def parse_index_pages_radia(self, response):
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        item = response.meta['item']
        cookie = response.meta['cookie']
        item['index_pages'][0]['data']['radia'] = float(
            convert_str(dict_result['result']['trendResult']['index']['score'][-1]))
        url = 'https://mp.yidianzixun.com/api/get-main-data'
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie,
                      callback=self.parse_index_pages_comment, dont_filter=True)

    def parse_index_pages_comment(self, response):
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        item = response.meta['item']
        cookie = response.meta['cookie']
        item['index_pages'][0]['data']['commentCount'] = int(dict_result['result']['main']['addCommentDoc'])
        item['index_pages'][0]['data']['likeCount'] = int(dict_result['result']['main']['likeDoc'])
        item['index_pages'][0]['data']['shareCount'] = int(dict_result['result']['main']['shareDoc'])
        item['index_pages'][0]['data']['contentCount'] = int(dict_result['result']['main']['postNum'])
        now_time = datetime.datetime.now()
        begin_time = (now_time + datetime.timedelta(days=-7)).strftime('%Y-%m-%d')
        url = 'https://mp.yidianzixun.com/api/source-data?date=%s&retdays=6' % begin_time
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie,
                      callback=self.parse_index_pages_all_articles, dont_filter=True)

    def parse_index_pages_all_articles(self, response):
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        item = response.meta['item']
        cookie = response.meta['cookie']
        item['index_pages'][0]['data']['dailies'] = []
        dalies = dict_result['result']
        for day_all_articles_logtime in dalies.keys():
            day_all_articles_dict = {}
            day_all_articles_dict['logtime'] = int(day_all_articles_logtime.replace('-', ''))
            day_all_articles_dict['pvCount'] = int(dalies[day_all_articles_logtime]['viewDoc'])
            day_all_articles_dict['readCount'] = int(dalies[day_all_articles_logtime]['clickDoc'])
            day_all_articles_dict['contentCount'] = int(dalies[day_all_articles_logtime]['postNum'])
            day_all_articles_dict['commentCount'] = int(dalies[day_all_articles_logtime]['addCommentDoc'])
            day_all_articles_dict['shareCount'] = int(dalies[day_all_articles_logtime]['shareDoc'])

            item['index_pages'][0]['data']['dailies'].append(day_all_articles_dict)
        end_time = str(int(round(time.time() * 1000)) - 24 * 60 * 60 * 1000 * 1)
        url = 'https://mp.yidianzixun.com/api/get-fans-detail?end_day=%s&ret_days=30' % end_time
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_user_pages,
                      dont_filter=True)

    def parse_user_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        user_pages = dict_result['result']
        for each_user_page_logtime in user_pages.keys():
            user_page = copy.deepcopy(self._single_item['user_page'])
            user_page['data']['logtime'] = int(each_user_page_logtime.replace('-', ''))
            user_page['data']['totalCount'] = int(user_pages[each_user_page_logtime]['fans_total'])
            user_page['data']['getCount'] = int(user_pages[each_user_page_logtime]['fans_add'])
            user_page['data']['loseCount'] = int(user_pages[each_user_page_logtime]['fans_reduce'])
            user_page['data']['gdCount'] = int(user_pages[each_user_page_logtime]['fans_pure_add'])
            user_page['data']['accountId'] = item['account']['accountId']
            item['user_pages'].append(user_page)
        url = 'https://mp.yidianzixun.com/api/settlement-system/cpm-income-info'
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_income_pages,
                      dont_filter=True)

    def parse_income_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        incomes = [dict_result['result']]
        for each_income in incomes:
            income_page = copy.deepcopy(self._single_item['income_page'])
            now_time = datetime.datetime.now()
            yesterday_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y%m%d')
            income_page['data']['logtime'] = int(yesterday_time)
            income_page['data']['total'] = 0.0 if each_income['monthlyCpmIncome'] == 'None' else float(
                each_income['monthlyCpmIncome'])
            income_page['data']['income'] = 0.0 if each_income['yesterdayCpmIncome'] == 'None' else float(
                each_income['yesterdayCpmIncome'])
            income_page['data']['accountId'] = item['account']['accountId']
            item['income_pages'].append(income_page)
        page_num = 1
        url = 'https://mp.yidianzixun.com/model/Statistic?page=%s&retdays=30&article_type=-5' % (
            page_num)
        yield Request(url, cookies=cookie,
                      meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                      callback=self.parse_content_pages_article, dont_filter=True)

    def parse_content_pages_article(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        content_pages = dict_result['posts']
        tota_page = dict_result['page_total']
        page_num = response.meta['page_num']

        if source_settings[self._source_name]['pages']['content_page'] != '':
            tota_page = int(source_settings[self._source_name]['pages']['content_page'])
        if page_num <= int(tota_page):
            page_num += 1
            url = 'https://mp.yidianzixun.com/model/Statistic?page=%s&retdays=30&article_type=-5' % (
                page_num)
            yield Request(url, cookies=cookie,
                          meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                          callback=self.parse_content_pages_article, dont_filter=True)
        elif page_num > int(tota_page):
            page_num = 1
            url = 'https://mp.yidianzixun.com/model/Statistic?page=%s&retdays=30&article_type=5' % (
                page_num)
            yield Request(url, cookies=cookie,
                          meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                          callback=self.parse_content_pages_movie, dont_filter=True)

        for each_content in content_pages:
            content_page = copy.deepcopy(self._single_item['content_page'])
            content_page['date'] = content_page['data']['logtime'] = int(
                time_stamp_to_time_format('%Y%m%d', int(each_content['date'][:10])))
            content_page['data']['type'] = 1
            content_page['data']['title'] = each_content['title']
            content_page['data']['pvCount'] = int(each_content['all_data']['viewDoc'])
            content_page['data']['readCount'] = int(each_content['all_data']['clickDoc'])
            content_page['data']['commentCount'] = int(each_content['all_data']['addCommentDoc'])
            content_page['data']['shareCount'] = int(each_content['all_data']['shareDoc'])
            content_page['data']['collectCount'] = int(each_content['all_data']['likeDoc'])
            content_page['data']['accountId'] = item['account']['accountId']
            content_page['data']['dailies'] = []
            item['content_pages'].append(content_page)

    def parse_content_pages_movie(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        content_pages = dict_result['posts']
        tota_page = dict_result['page_total']
        page_num = response.meta['page_num']

        if source_settings[self._source_name]['pages']['content_page'] != '':
            tota_page = int(source_settings[self._source_name]['pages']['content_page'])
        if page_num <= int(tota_page):
            page_num += 1
            url = 'https://mp.yidianzixun.com/model/Statistic?page=%s&retdays=30&article_type=5' % (
                page_num)
            yield Request(url, cookies=cookie,
                          meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                          callback=self.parse_content_pages_movie, dont_filter=True)
        elif page_num > int(tota_page):
            logging.info('spider account %s finished' % item['account']['user_name'])
            yield item
            driver_factory = SeleniumDirverFactory()
            driver_factory.quit_driver()

        for each_content in content_pages:
            content_page = copy.deepcopy(self._single_item['content_page'])
            content_page['date'] = content_page['data']['logtime'] = int(
                time_stamp_to_time_format('%Y%m%d', int(each_content['date'][:10])))
            content_page['data']['type'] = 2
            content_page['data']['title'] = each_content['title']
            content_page['data']['pvCount'] = int(each_content['all_data']['viewDoc'])
            content_page['data']['readCount'] = int(each_content['all_data']['clickDoc'])
            content_page['data']['commentCount'] = int(each_content['all_data']['addCommentDoc'])
            content_page['data']['shareCount'] = int(each_content['all_data']['shareDoc'])
            content_page['data']['collectCount'] = int(each_content['all_data']['likeDoc'])
            content_page['data']['accountId'] = item['account']['accountId']
            content_page['data']['dailies'] = []
            item['content_pages'].append(content_page)
