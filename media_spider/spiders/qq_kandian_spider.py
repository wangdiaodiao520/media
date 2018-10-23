#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import copy
import datetime
import logging
import time
import traceback

from scrapy import Request

from media_spider.conf.all_spider_conf import qi_e_conf, qq_kandian_conf
from media_spider.spiders.common_spider import CommonSpider
from media_spider.tools.phantom_js_driver import SeleniumDirverFactory
from media_spider.tools.time_tools import get_time_format
from media_spider.util.basic_type_converter import from_string_to_json
from media_spider.util.consts import all_pages, source_settings
from media_spider.util.convert_util import convert_str, convert_str_content


class QQKanDianSpider(CommonSpider):
    name = 'qq_kandian_spider'
    _source_name = 'qq_kandian'
    _platformId = None
    _dt = None
    _single_item = {}
    _account = 'qq_kandian_account'

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/json, text/javascript, */*; q=0.01,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
    }

    def after_login(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        try:
            index_count = self.x_path(response, qq_kandian_conf['index_page']['radia'])[0].encode('utf-8')
            fans_count = self.x_path(response, qq_kandian_conf['index_page']['fanCount'])[0].encode('utf-8')
            readCount = self.x_path(response, qq_kandian_conf['index_page']['readCount'])[0].encode('utf-8')
            play_count = self.x_path(response, qq_kandian_conf['index_page']['play_count'])[0].encode('utf-8')
        except:
            traceback.print_exc()
            logging.error('login failed or site templet is out-of-date')
        index_pages = [
            {'radia': index_count, 'fanCount': fans_count, 'readCount': readCount, 'play_count': play_count}]
        for each_index_page in index_pages:
            index_page = copy.deepcopy(self._single_item['index_page'])
            index_page['data']['logtime'] = int(index_page['date'])
            index_page['data']['radia'] = float(each_index_page['radia'])
            multiplier_num = 10000 if each_index_page['readCount'][-1] == 'w' else 1
            index_page['data']['fanCount'] = int(float(each_index_page['fanCount'].replace('w', '')) * multiplier_num)
            index_page['data']['readCount'] = int(float(each_index_page['readCount'].replace('w', '')) * multiplier_num)
            index_page['data']['play_count'] = int(float(each_index_page['play_count'].replace('w', '')) * multiplier_num)
            index_page['data']['accountId'] = item['account']['accountId']
            item['index_pages'].append(index_page)
        now_time = datetime.datetime.now()
        begin_time = (now_time + datetime.timedelta(days=-8)).strftime('%Y-%m-%d')
        end_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        url = 'https://kandian.mp.qq.com/api/analysis_article/get-all-list?type=0&start_date=%s&end_date=%s' % (
            begin_time, end_time)

        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie,
                      callback=self.parse_index_pages_all_articles, dont_filter=True)

    def parse_index_pages_all_articles(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        item['index_pages'][0]['data']['dailies'] = []
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        dalies = dict_result['data']['detailed']
        for day_all_articles in dalies:
            day_all_articles_dict = {}
            day_all_articles_dict['logtime'] = int(day_all_articles['date'].replace('-', ''))
            day_all_articles_dict['readCount'] = int(
                convert_str(day_all_articles['read']['total']['read_times'].encode('utf-8')))
            day_all_articles_dict['likeCount'] = int(convert_str(day_all_articles['biu']['read_times'].encode('utf-8')))
            day_all_articles_dict['shareCount'] = int(
                convert_str(day_all_articles['share']['read_times'].encode('utf-8')))
            day_all_articles_dict['commentCount'] = int(
                convert_str(day_all_articles['comment']['read_times'].encode('utf-8')))
            day_all_articles_dict['collectCount'] = int(
                convert_str(day_all_articles['collection']['read_times'].encode('utf-8')))
            item['index_pages'][0]['data']['dailies'].append(day_all_articles_dict)

        now_time = datetime.datetime.now()
        end_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        begin_time = (now_time + datetime.timedelta(days=-31)).strftime('%Y-%m-%d')
        url = 'https://kandian.mp.qq.com/api/analysis_fans/fans_growth?isCompare=0&sDate=%s&eDate=%s' \
              '&compareStartDate=2018-06-25&compareEndDate=2018-07-01&sortOrder=0&type=2' % (
                  begin_time, end_time)
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_user_pages,
                      dont_filter=True)

    def parse_user_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        user_pages = dict_result['mainChart']
        for each_user_page in user_pages:
            user_page = copy.deepcopy(self._single_item['user_page'])
            user_page['data']['logtime'] = int(time.strftime("%Y%m%d", time.localtime(int(each_user_page['sendDate']))))
            user_page['data']['totalCount'] = int(each_user_page['data'][0]['totalFollowCount'])
            user_page['data']['getCount'] = int(each_user_page['data'][0]['newFollowCount'])
            user_page['data']['gdCount'] = int(each_user_page['data'][0]['addedFollowCount'])
            user_page['data']['loseCount'] = int(each_user_page['data'][0]['unfollowCount'])
            user_page['data']['accountId'] = item['account']['accountId']
            item['user_pages'].append(user_page)
        bigin_date = get_time_format('%Y-%m-%d', -30)
        end_date = get_time_format('%Y-%m-%d', -1)
        url = 'https://mp.qq.com/api/revenue/get_table_detail?current=1&every=50&start_date=%s&end_date=%s&' % (bigin_date, end_date)
        yield Request(url, cookies=cookie, meta={'item': item, 'cookie': cookie}, callback=self.parse_income_pages,
                      dont_filter=True)

    def parse_income_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        incomes = dict_result['data']['list']
        try:
            for each_income in incomes:
                income_page = copy.deepcopy(self._single_item['income_page'])
                income_page['data']['logtime'] = int(
                    convert_str(each_income['date'].replace('-', '')))
                income_page['data']['total'] = float(
                    convert_str(each_income['total_income']))
                income_page['data']['income'] = float(
                    convert_str(each_income['basic_income']))
                income_page['data']['allowance'] = float(
                    convert_str(each_income['bonus_income']))
                income_page['data']['accountId'] = item['account']['accountId']
                item['income_pages'].append(income_page)
        except:
            logging.error('income pages error,to check')
            traceback.print_exc()
            pass
        url = 'https://kandian.mp.qq.com/api/analysis_article/get-single-list?current=1&every=50&start_date=2018-07-12&end_date=2018-07-18'
        yield Request(url, cookies=cookie, meta={'item': item, 'cookie': cookie, 'page_num': 1},
                      callback=self.parse_content_pages_article, dont_filter=True)

    def parse_content_pages_article(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        content_pages = dict_result['data']
        try:
            total_num = int(dict_result['total'])
            tota_page = total_num / 50 if total_num % 50 == 0 else total_num / 50 + 1
        except:
            logging.error('parse_content_pages_article error')
        page_num = response.meta['page_num']
        if source_settings[self._source_name]['pages']['content_page'] != '':
            tota_page = int(source_settings[self._source_name]['pages']['content_page'])
        if page_num <= int(tota_page):
            page_num += 1
            now_time = datetime.datetime.now()
            begin_time = (now_time + datetime.timedelta(days=-31 * 12 * 5)).strftime('%Y-%m-%d')
            end_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
            url = 'https://kandian.mp.qq.com/api/analysis_article/get-single-list?current=%s&every=50&start_date=%s&end_date=%s' % (
                page_num, begin_time, end_time)
            yield Request(url, cookies=cookie,
                          meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                          callback=self.parse_content_pages_article, dont_filter=True)
        elif page_num > int(tota_page):
            page_num = 1
            now_time = datetime.datetime.now()
            begin_time = (now_time + datetime.timedelta(days=-31 * 12 * 5)).strftime('%Y-%m-%d')
            end_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
            url = 'https://kandian.mp.qq.com/api/analysis_video/get-single-list?current=%s&every=50&type=0&start_date=%s&end_date=%s' % (
                page_num, begin_time, end_time)
            yield Request(url, cookies=cookie,
                          meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                          callback=self.parse_content_pages_movie, dont_filter=True)

        for each_content in content_pages:
            content_page = copy.deepcopy(self._single_item['content_page'])
            content_page['date'] = content_page['data']['logtime'] = int(
                convert_str_content(each_content['send_time'][:len('2018-01-01')].encode(
                    'utf-8')).replace('-', ''))
            content_page['data']['type'] = 1
            content_page['data']['title'] = each_content['title']
            content_page['data']['readCount'] = int(convert_str_content(each_content['total_readtimes'].encode('utf-8')))
            content_page['data']['shareCount'] = int(convert_str_content(each_content['share'].encode('utf-8')))
            content_page['data']['accountId'] = item['account']['accountId']
            content_page['data']['dailies'] = []
            rowkey = each_content['rowkey']
            url = 'https://kandian.mp.qq.com/page/analysis_article/article_single_detail?id=%s' % rowkey + '#2'
            yield Request(url, cookies=cookie, meta=content_page,
                          callback=self.parse_content_pages_detail_article)
            item['content_pages'].append(content_page)

    def parse_content_pages_detail_article(self, response):
        content_page = response.meta
        content_pages = response.xpath("//table[@id='testTable_mix']/tbody/tr")
        for single_content_page in content_pages:
            single_content_page_dict = {}
            single_content_page_dict['logtime'] = int(
                convert_str(single_content_page.xpath("./td[1]/text()").extract()[0].encode(
                    'utf-8')))
            single_content_page_dict['readCount'] = int(
                convert_str(single_content_page.xpath("./td[2]/text()").extract()[0].encode(
                    'utf-8')))
            single_content_page_dict['likeCount'] = int(
                convert_str(single_content_page.xpath("./td[4]/text()").extract()[0].encode(
                    'utf-8')))
            single_content_page_dict['shareCount'] = int(
                convert_str(single_content_page.xpath("./td[6]/text()").extract()[0].encode(
                    'utf-8')))
            single_content_page_dict['commentCount'] = int(
                convert_str(single_content_page.xpath("./td[8]/text()").extract()[0].encode(
                    'utf-8')))
            content_page['data']['dailies'].append(single_content_page_dict)

    def parse_content_pages_movie(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        content_pages = dict_result['data']
        page_num = response.meta['page_num']
        try:
            total_num = int(dict_result['total'])
            tota_page = total_num / 50 if total_num % 50 == 0 else total_num / 50 + 1
        except:
            logging.error('parse_content_pages_article error')
        if source_settings[self._source_name]['pages']['content_page'] != '':
            tota_page = int(source_settings[self._source_name]['pages']['content_page'])
        if page_num <= int(tota_page):
            page_num += 1
            now_time = datetime.datetime.now()
            begin_time = (now_time + datetime.timedelta(days=-31 * 12 * 5)).strftime('%Y-%m-%d')
            end_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
            url = 'https://kandian.mp.qq.com/api/analysis_video/get-single-list?current=%s&every=50&type=0&start_date=%s&end_date=%s' % (
                page_num, begin_time, end_time)
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
                convert_str_content(each_content['send_time'][:len('2018-01-01')].encode(
                    'utf-8')).replace('-', ''))
            content_page['data']['type'] = 2
            content_page['data']['title'] = each_content['title']
            content_page['data']['readCount'] = int(convert_str_content(each_content['total_readtimes'].encode('utf-8')))
            content_page['data']['shareCount'] = int(convert_str_content(each_content['share'].encode('utf-8')))
            content_page['data']['accountId'] = item['account']['accountId']
            content_page['data']['dailies'] = []
            item['content_pages'].append(content_page)

