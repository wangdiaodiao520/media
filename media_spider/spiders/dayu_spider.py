#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import copy
import logging
import traceback

from scrapy import Request

from media_spider.spiders.common_spider import CommonSpider
from media_spider.tools.time_tools import get_time_format, get_time_stamp_13
from media_spider.util.basic_type_converter import from_string_to_json
from media_spider.util.consts import source_settings


class DaYuSpider(CommonSpider):
    name = 'dayu_spider'
    _source_name = 'dayu'
    _platformId = None
    _dt = None
    _single_item = {}
    _account = 'dayu_account'

    custom_settings = {
        'DOWNLOAD_DELAY': '1',
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
        begin_date = get_time_format("%Y%m%d", -2)
        end_date = get_time_format("%Y%m%d", -1)
        url = 'https://mp.dayu.com/dashboard/feature/star/starinfo?beginDate=%s&endDate=%s' % (begin_date, end_date)
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_index_pages_radia,
                      dont_filter=True)

    def parse_index_pages_radia(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        try:
            dict_result = from_string_to_json(response.text.encode('utf-8'))
            index_pages = [{'radia': dict_result['data'][0]['total_score']}]
        except:
            traceback.print_exc()
            logging.error('login failed or site templet is out-of-date, error info %s' % response.text.encode('utf-8'))
        for each_index_page in index_pages:
            index_page = copy.deepcopy(self._single_item['index_page'])
            index_page['data']['logtime'] = int(index_page['date'])
            index_page['data']['radia'] = float(each_index_page['radia'])
            index_page['data']['accountId'] = item['account']['accountId']
            item['index_pages'].append(index_page)
        bigin_date = get_time_format('%Y-%m-%d', -7)
        end_date = get_time_format('%Y-%m-%d', -1)
        time_stamp_13 = get_time_stamp_13()
        url = 'https://mp.dayu.com/api/stat/article/all/daylist?beginDate=%s&endDate=%s&origin=manual&_=%s' % (bigin_date, end_date,time_stamp_13)
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_index_pages_all_articles,
                      dont_filter=True)

    def parse_index_pages_all_articles(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        dalies = dict_result['data']['list']
        for day_all_articles in dalies:
            day_all_articles_dict = {}
            day_all_articles_dict['logtime'] = int(day_all_articles['date'].replace('-', ''))
            day_all_articles_dict['pvCount'] = int(day_all_articles['show_pv'])
            day_all_articles_dict['readCount'] = int(day_all_articles['click_pv'])
            day_all_articles_dict['commentCount'] = int(day_all_articles['cmt_pv'])
            day_all_articles_dict['likeCount'] = int(day_all_articles['like_pv'])
            day_all_articles_dict['collectCount'] = int(day_all_articles['fav_pv'])
            day_all_articles_dict['shareCount'] = int(day_all_articles['share_pv'])
            item['index_pages'][0]['data']['dailies'].append(day_all_articles_dict)

        bigin_date = get_time_format('%Y-%m-%d', -7)
        end_date = get_time_format('%Y-%m-%d', -1)
        time_stamp_13 = get_time_stamp_13()
        url = 'https://mp.dayu.com/api/stat/user/fans/daylist?beginDate=%s&endDate=%s&source=uc&_=%s' \
              % (bigin_date, end_date, time_stamp_13)
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_user_pages,dont_filter=True)

    def parse_user_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        user_pages = dict_result['data']['list']
        for each_user_page in user_pages:
            user_page = copy.deepcopy(self._single_item['user_page'])
            user_page['data']['logtime'] = int(each_user_page['date'].replace('-', ''))
            user_page['data']['totalCount'] = int(each_user_page['total_follow_uv'])
            user_page['data']['getCount'] = int(each_user_page['follow_uv'])
            user_page['data']['loseCount'] = int(each_user_page['unfollow_uv'])
            user_page['data']['gdCount'] = int(each_user_page['follow_increase'])
            user_page['data']['accountId'] = item['account']['accountId']
            item['user_pages'].append(user_page)
        url = 'https://mp.dayu.com/dashboard/unifiedSettlement/getJournals'
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie,
                      callback=self.parse_income_pages,
                      dont_filter=True)

    def parse_income_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        incomes_tmp = dict_result['data']
        repeat_income_filter = {}
        for each_income in incomes_tmp:
            log_time_tmp = int(each_income['created_at'][:len('2018-01-01')].replace('-', ''))
            total = float(each_income['aftertax_amount'])
            if log_time_tmp in repeat_income_filter:
                repeat_income_filter[log_time_tmp]['total'] += total
                continue
            repeat_income_filter[log_time_tmp] = {}
            repeat_income_filter[log_time_tmp]['total'] = total

        for log_time_tmp in repeat_income_filter:
            income_page = copy.deepcopy(self._single_item['income_page'])
            income_page['data']['logtime'] = log_time_tmp
            income_page['data']['total'] = repeat_income_filter[log_time_tmp]['total']
            income_page['data']['accountId'] = item['account']['accountId']
            item['income_pages'].append(income_page)

        bigin_date = get_time_format('%Y-%m-%d', -90)
        end_date = get_time_format('%Y-%m-%d', -1)
        time_stamp_13 = get_time_stamp_13()
        page_num = 1
        url = 'https://mp.dayu.com/api/stat/article/detail/articlelist?beginDate=%s&endDate=%s&origin=manual&page=%s&_=%s' \
              % (bigin_date, end_date, page_num, time_stamp_13)
        yield Request(url, meta={'page_num': page_num, 'item': item, 'cookie': cookie}, cookies=cookie,
                      callback=self.parse_content_pages_article,
                      dont_filter=True)


    def parse_content_pages_article(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        content_pages = dict_result['data']
        tota_page = dict_result['total']
        page_num = response.meta['page_num']

        if source_settings[self._source_name]['pages']['content_page'] != '':
            tota_page = source_settings[self._source_name]['pages']['content_page']
        if page_num <= int(tota_page):
            page_num += 1
            bigin_date = get_time_format('%Y-%m-%d', -90)
            end_date = get_time_format('%Y-%m-%d', -1)
            time_stamp_13 = get_time_stamp_13()
            url = 'https://mp.dayu.com/api/stat/article/detail/articlelist?beginDate=%s&endDate=%s&origin=manual&page=%s&_=%s' \
                  % (bigin_date, end_date, page_num, time_stamp_13)
            yield Request(url, cookies=cookie,
                          meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                          callback=self.parse_content_pages_article, dont_filter=True)
        elif page_num > int(tota_page):
            logging.info('spider account %s finished' % item['account']['user_name'])
            yield item

        for each_content in content_pages:
            content_page = copy.deepcopy(self._single_item['content_page'])
            content_page['date'] = content_page['data']['logtime'] = int(
                each_content['publish_at'][:len('2018-01-01')].replace(
                    '-', ''))
            content_page['data']['type'] = 1
            content_page['data']['title'] = each_content['title']
            content_page['data']['readCount'] = int(each_content['click_pv'])
            content_page['data']['commentCount'] = int(each_content['cmt_pv'])
            content_page['data']['pvCount'] = int(each_content['show_pv'])
            content_page['data']['likeCount'] = int(each_content['like_pv'])
            content_page['data']['collectCount'] = int(each_content['fav_pv'])
            content_page['data']['shareCount'] = int(each_content['share_pv'])
            content_page['data']['accountId'] = item['account']['accountId']
            content_page['data']['dailies'] = []
            item['content_pages'].append(content_page)

