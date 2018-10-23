#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import copy
import datetime
import logging
import time
import traceback

from scrapy import Request

from media_spider.conf.all_spider_conf import qi_e_conf
from media_spider.spiders.common_spider import CommonSpider
from media_spider.tools.phantom_js_driver import SeleniumDirverFactory
from media_spider.tools.time_tools import get_time_format
from media_spider.util.basic_type_converter import from_string_to_json
from media_spider.util.consts import source_settings


class QiESpider(CommonSpider):
    name = 'qi_e_spider'
    _source_name = 'qi_e'
    _platformId = None
    _dt = None
    _single_item = {}
    _account = 'qi_e_account'

    def after_login(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        try:
            qi_e_index_number = self.x_path(response, qi_e_conf['index_page']['radia'])[3].encode('utf-8')
            index_page_qi_e_index_number = float(qi_e_index_number.replace(' ', '').replace('\n', '').replace(',', ''))
            index_pages = [{'radia': index_page_qi_e_index_number}]
        except:
            traceback.print_exc()
            logging.error('login failed or site templet is out-of-date')
        for each_index_page in index_pages:
            index_page = copy.deepcopy(self._single_item['index_page'])
            index_page['data']['logtime'] = int(index_page['date'])
            index_page['data']['radia'] = float(each_index_page['radia'])
            index_page['data']['accountId'] = item['account']['accountId']
            item['index_pages'].append(index_page)
        begin_time = str(time.time() - 24 * 60 * 60 * 8)[:10]
        end_time = str(time.time() - 24 * 60 * 60 * 1)[:10]
        url = 'https://om.qq.com/statistic/mediaDaily?channel=0&btime=%s&etime=%s&page=1&num=1000&relogin=1' % (
            begin_time, end_time)
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie,
                      callback=self.parse_index_pages_all_articles,
                      dont_filter=True)

    def parse_index_pages_all_articles(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        item['index_pages'][0]['data']['dailies'] = []
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        dalies = dict_result['data']['statistic']
        for day_all_articles in dalies:
            day_all_articles_dict = {}
            day_all_articles_dict['logtime'] = int(day_all_articles['statistic_date'].replace('-', ''))
            day_all_articles_dict['pvCount'] = int(day_all_articles['exposure'])
            day_all_articles_dict['readCount'] = int(day_all_articles['read'])
            day_all_articles_dict['collectCount'] = int(day_all_articles['collect'])
            day_all_articles_dict['shareCount'] = int(day_all_articles['relay'])
            item['index_pages'][0]['data']['dailies'].append(day_all_articles_dict)

        begin_time = str(time.time() - 24 * 60 * 60 * 8)[:10]
        end_time = str(time.time() - 24 * 60 * 60 * 1)[:10]
        url = 'https://om.qq.com/Statistic/subscribeDaily?media=%s&channel=0&fields=fdate,subs_cnt_total,' \
              'subs_cnt_today,unsubs_cnt_today&btime=%s&etime=%s&page=1&num=8&merge=0&relogin=1' % (
                  cookie[u'userid'], begin_time, end_time)
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_user_pages)

    def parse_user_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        json_str = response.text.encode('utf-8')
        json_str = json_str.replace(
            '<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '').replace(
            '</pre></body></html>', '')
        dict_result = from_string_to_json(json_str)
        user_pages = dict_result['data']['statistic']
        for each_user_page in user_pages:
            user_page = copy.deepcopy(self._single_item['user_page'])
            user_page['data']['logtime'] = int(each_user_page['fdate'].replace('-', ''))
            user_page['data']['totalCount'] = int(each_user_page['subs_cnt_total'])
            user_page['data']['getCount'] = int(each_user_page['subs_cnt_today'])
            user_page['data']['loseCount'] = int(each_user_page['unsubs_cnt_today'])
            user_page['data']['accountId'] = item['account']['accountId']
            item['user_pages'].append(user_page)
        now_time = datetime.datetime.now()
        end_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        begin_time = (now_time + datetime.timedelta(days=-31)).strftime('%Y-%m-%d')
        url = 'https://om.qq.com/income/GetUserIncomeList?from=%s&to=%s&relogin=1' % (begin_time, end_time)
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_income_pages,
                      dont_filter=True)

    def parse_income_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        incomes = dict_result['data']
        for each_income in incomes:
            income_page = copy.deepcopy(self._single_item['income_page'])
            income_page['data']['logtime'] = int(each_income['date'].replace('-', ''))
            income_page['data']['total'] = -2.0 if each_income['total_amount'] == '--' else float(
                each_income['total_amount'])
            income_page['data']['allowance'] = -2.0 if each_income['total_platform_amount'] == '--' else float(
                each_income['total_platform_amount'])
            income_page['data']['income'] = -2.0 if each_income['total_content_amount'] == '--' else float(
                each_income['total_content_amount'])
            income_page['data']['accountId'] = item['account']['accountId']
            item['income_pages'].append(income_page)
        end_time = str(time.time())[:10]
        page_num = 1
        url = 'https://om.qq.com/statistic/ArticleReal?page=%s&num=8&btime=1420041600&etime=%s&relogin=1' % (
            page_num, end_time)
        yield Request(url, cookies=cookie,
                      meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                      callback=self.parse_content_pages_article, dont_filter=True)


    def parse_content_pages_article(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        content_pages = dict_result['data']['statistic']
        tota_page = dict_result['data']['totalPage']
        page_num = response.meta['page_num']

        if source_settings[self._source_name]['pages']['content_page'] != '':
            tota_page = int(source_settings[self._source_name]['pages']['content_page'])
        if page_num <= int(tota_page):
            page_num += 1
            end_time = str(time.time())[:10]
            url = 'https://om.qq.com/statistic/ArticleReal?page=%s&num=8&btime=1420041600&etime=%s&relogin=1' % (
                page_num, end_time)
            yield Request(url, cookies=cookie,
                          meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                          callback=self.parse_content_pages_article, dont_filter=True)
        elif page_num > int(tota_page):
            page_num = 1
            begin_date = get_time_format('%Y-%m-%d', -6)
            end_date = get_time_format('%Y-%m-%d')
            url = 'https://om.qq.com/VideoData/MediaVideoList?startdate=%s&enddate=%s&limit=8&page=%s&fields=2%%7C3&source=0&relogin=1' % (
                begin_date, end_date, page_num)
            yield Request(url, cookies=cookie,
                          meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                          callback=self.parse_content_pages_movie, dont_filter=True)

        for each_content in content_pages:
            content_page = copy.deepcopy(self._single_item['content_page'])
            content_page['date'] = content_page['data']['logtime'] = int(
                each_content['pubTime'][:len('2018-01-01')].replace(
                    '-', ''))
            content_page['data']['type'] = 1
            content_page['data']['title'] = each_content['title']
            content_page['data']['readCount'] = int(each_content['read'])
            content_page['data']['pvCount'] = int(each_content['exposure'])
            content_page['data']['accountId'] = item['account']['accountId']
            content_page['data']['dailies'] = []
            articleId = each_content['articleId']
            begin_time = 1421164800
            end_time = str(time.time() - 24 * 60 * 60 * 1)[:10]
            url = 'https://om.qq.com/statistic/ArticleAnalyze?media=%s&article=%s&channel=0&' \
                  'fields=title,read,exposure,relay,collect,postil,updating,comment,read_uv,vv&titleType=0&btime=%s&etime=%s&' \
                  'page=1&num=1000&merge=0&relogin=1' % (
                      cookie[u'userid'], articleId, begin_time, end_time)
            yield Request(url, cookies=cookie, meta=content_page,
                          callback=self.parse_content_pages_detail_article)
            item['content_pages'].append(content_page)

    def parse_content_pages_detail_article(self, response):
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        content_pages = dict_result['data']['statistic']
        content_page = response.meta
        for single_content_page in content_pages:
            single_content_page_dict = {}
            single_content_page_dict['logtime'] = int(single_content_page['statistic_date'].replace('-', ''))
            single_content_page_dict['readCount'] = int(single_content_page['read'])
            single_content_page_dict['pvCount'] = int(single_content_page['exposure'])
            single_content_page_dict['shareCount'] = int(single_content_page['relay'])
            single_content_page_dict['collectCount'] = int(single_content_page['collect'])
            content_page['data']['dailies'].append(single_content_page_dict)

    def parse_content_pages_movie(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        content_pages = dict_result['data']['list']
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
            begin_date = get_time_format('%Y-%m-%d', -6)
            end_date = get_time_format('%Y-%m-%d')
            url = 'https://om.qq.com/VideoData/MediaVideoList?startdate=%s&enddate=%s&limit=8&page=%s&fields=2%%7C3&source=0&relogin=1' % (
                begin_date, end_date, page_num)
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
                each_content['uploadtime'][:len('2018-01-01')].replace(
                    '-', ''))
            content_page['data']['type'] = 2
            content_page['data']['title'] = each_content['title']
            content_page['data']['readCount'] = int(each_content['new_total_play_pv'])
            content_page['data']['accountId'] = item['account']['accountId']
            content_page['data']['dailies'] = []
            vid = each_content['vid']
            begin_time = get_time_format('%Y-%m-%d', -1000)
            end_time = get_time_format('%Y-%m-%d')
            url = 'https://om.qq.com/VideoData/VideoDailyList?vid=%s&fields=2%%7C7&source=0&startdate=%s&enddate=%s&relogin=1' % (
                      vid, begin_time, end_time)
            yield Request(url, cookies=cookie, meta=content_page,
                          callback=self.parse_content_pages_detail_movie)
            item['content_pages'].append(content_page)

    def parse_content_pages_detail_movie(self, response):
        json_str = response.text.encode('utf-8')
        dict_result = from_string_to_json(json_str)
        content_pages = dict_result['data']['list']
        content_page = response.meta
        for single_content_page in content_pages:
            single_content_page_dict = {}
            single_content_page_dict['logtime'] = int(single_content_page['date'].replace('-', ''))
            single_content_page_dict['readCount'] = int(single_content_page['new_daily_play_pv'])
            content_page['data']['dailies'].append(single_content_page_dict)
