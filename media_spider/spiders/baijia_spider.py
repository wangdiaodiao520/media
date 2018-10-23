#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
import copy
import logging
import traceback

from scrapy import Request, FormRequest

from media_spider.spiders.common_spider import CommonSpider
from media_spider.tools.phantom_js_driver import SeleniumDirverFactory
from media_spider.tools.time_tools import get_time_format
from media_spider.util.basic_type_converter import from_string_to_json
from media_spider.util.consts import source_settings


class BaiJiaSpider(CommonSpider):
    name = 'bai_jia_spider'
    _source_name = 'bai_jia'
    _platformId = None
    _dt = None
    _single_item = {}
    _account = 'bai_jia_account'

    custom_settings = {
        'DOWNLOAD_DELAY': '3',
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
        url = 'https://baijiahao.baidu.com/builderinner/api/content/app/userScore'
        yield FormRequest(
            url=url,
            method='POST',
            callback=self.parse_index_pages_radia,
            cookies=cookie,
            meta={'item': item, 'cookie': cookie},
            dont_filter=True
        )

    def parse_index_pages_radia(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        try:
            dict_result = from_string_to_json(response.text.encode('utf-8'))
            index_pages = [{'radia': dict_result['data']['score_info']['score'],
                            'logtime': dict_result['data']['score_info']['score_date']}]
        except:
            traceback.print_exc()
            logging.error('login failed or site templet is out-of-date')
        for each_index_page in index_pages:
            index_page = copy.deepcopy(self._single_item['index_page'])
            index_page['data']['radia'] = int(each_index_page['radia'])
            index_page['data']['logtime'] = int(each_index_page['logtime'])
            index_page['data']['accountId'] = item['account']['accountId']
            item['index_pages'].append(index_page)
        url = 'https://baijiahao.baidu.com/builder/author/home/index?'
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie,
                      callback=self.parse_index_pages_count_all,
                      dont_filter=True)

    def parse_index_pages_count_all(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        item['index_pages'][0]['data']['fanCount'] = int(dict_result['data']['coreData']['fansCount'])
        item['index_pages'][0]['data']['readCount'] = int(dict_result['data']['coreData']['viewCount'])
        bigin_date = get_time_format('%Y%m%d', -7)
        end_date = get_time_format('%Y%m%d', -1)
        url = 'https://baijiahao.baidu.com/builder/author/statistic/appStatistic'
        yield FormRequest(
            url=url,
            callback=self.parse_index_pages_all_articles,
            formdata={'type': 'news', 'is_yesterday': 'false', 'start_day': bigin_date, 'end_day': end_date,
                      'stat': '0'},
            meta={'item': item, 'cookie': cookie},
            cookies=cookie,
            dont_filter=True
        )

    def parse_index_pages_all_articles(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        item['index_pages'][0]['data']['dailies'] = []
        dalies = dict_result['data']['list']
        for day_all_articles in dalies:
            day_all_articles_dict = {}
            day_all_articles_dict['logtime'] = int(day_all_articles['event_day'])
            day_all_articles_dict['pvCount'] = int(day_all_articles['recommend_count'])
            day_all_articles_dict['readCount'] = int(day_all_articles['view_count'])
            day_all_articles_dict['commentCount'] = int(day_all_articles['comment_count'])
            day_all_articles_dict['likeCount'] = int(day_all_articles['likes_count'])
            day_all_articles_dict['collectCount'] = int(day_all_articles['collect_count'])
            day_all_articles_dict['shareCount'] = int(day_all_articles['share_count'])
            item['index_pages'][0]['data']['dailies'].append(day_all_articles_dict)

        bigin_date = get_time_format('%Y%m%d', -7)
        end_date = get_time_format('%Y%m%d', -1)
        url = 'https://baijiahao.baidu.com/builder/author/statistic/getFansBasicInfo?start=%s&end=%s&fans_type=new%%2Csum&sort=asc&is_page=0&show_type=chart' % (
            bigin_date, end_date)
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_user_pages)

    def parse_user_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        user_pages = dict_result['data']['list']
        for each_user_page in user_pages:
            user_page = copy.deepcopy(self._single_item['user_page'])
            user_page['data']['logtime'] = int(each_user_page['day'])
            user_page['data']['totalCount'] = int(each_user_page['sum_fans_count'])
            user_page['data']['gdCount'] = int(each_user_page['new_fans_count'])
            user_page['data']['accountId'] = item['account']['accountId']
            item['user_pages'].append(user_page)
        bigin_date = get_time_format(days_compare=-8, begining_day_time=True)
        end_date = get_time_format(days_compare=-2, begining_day_time=True)
        url = 'https://baijiahao.baidu.com/builder/author/income/incomeBaseInfo?startDate=%s&endDate=%s&pageIndex=1&num=10&listType=0&is_export=0' % (
            bigin_date, end_date)
        yield Request(url, meta={'item': item, 'cookie': cookie}, cookies=cookie, callback=self.parse_income_pages,
                      dont_filter=True)

    def parse_income_pages(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        income_pages = dict_result['data']
        for each_income_page_logtime in income_pages.keys():
            income_page = copy.deepcopy(self._single_item['income_page'])
            income_page['data']['logtime'] = int(
                get_time_format(format_str='%Y%m%d', check_time_stamp=int(each_income_page_logtime)))
            income_page['data']['total'] = float(income_pages[each_income_page_logtime]['total_income'])
            income_page['data']['income'] = float(income_pages[each_income_page_logtime]['ad_income'])
            income_page['data']['allowance'] = float(income_pages[each_income_page_logtime]['subsidy_income'])
            income_page['data']['accountId'] = item['account']['accountId']
            item['income_pages'].append(income_page)
        page_num = 1
        url = 'https://baijiahao.baidu.com/builder/article/lists?type=&collection=publish&pageSize=10&currentPage=%s&search=' % (
            page_num)
        yield Request(url, cookies=cookie,
                      meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                      callback=self.parse_content_pages_article, dont_filter=True)

    def parse_content_pages_article(self, response):
        item = response.meta['item']
        cookie = response.meta['cookie']
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        content_pages = dict_result['data']['list']
        tota_page = dict_result['data']['page']['totalPage']
        page_num = response.meta['page_num']

        if source_settings[self._source_name]['pages']['content_page'] != '':
            tota_page = source_settings[self._source_name]['pages']['content_page']
        if page_num <= int(tota_page):
            page_num += 1
            url = 'https://baijiahao.baidu.com/builder/article/lists?type=&collection=publish&pageSize=10&currentPage=%s&search=' % (
                page_num)
            yield Request(url, cookies=cookie,
                          meta={'page_num': page_num, 'item': item, 'cookie': cookie},
                          callback=self.parse_content_pages_article, dont_filter=True)
        elif page_num > int(tota_page):
            logging.info('spider account %s finished' % item['account']['user_name'])
            yield item
            driver_factory = SeleniumDirverFactory()
            driver_factory.quit_driver()

        for each_content in content_pages:
            content_page = copy.deepcopy(self._single_item['content_page'])
            content_page['date'] = content_page['data']['logtime'] = int(
                each_content['publish_time'][:len('2018-01-01')].replace(
                    '-', ''))
            if each_content['type'] == 'news':
                content_page['data']['type'] = 1
            elif each_content['type'] == 'video':
                content_page['data']['type'] = 2
            else:
                logging.error('content type error to check')
            content_page['data']['title'] = each_content['title']
            content_page['data']['readCount'] = int(each_content['read_amount'])
            content_page['data']['collectCount'] = int(each_content['collection_amount'])
            content_page['data']['pvCount'] = int(each_content['rec_amount'])
            content_page['data']['shareCount'] = int(each_content['share_amount'])
            content_page['data']['commentCount'] = int(each_content['comment_amount'])
            content_page['data']['likeCount'] = int(each_content['like_amount'])
            content_page['data']['accountId'] = item['account']['accountId']
            content_page['data']['dailies'] = []
            articleId = each_content['transform_id']
            url = 'https://baijiahao.baidu.com/builder/author/statistic/articleDailyListStatistic'
            yield FormRequest(
                url=url,
                callback=self.parse_content_pages_detail_article,
                formdata={'article_id': articleId, 'start_day': '0', 'end_day': '0'},
                meta=content_page,
                cookies=cookie,
                dont_filter=True
            )
            item['content_pages'].append(content_page)

    def parse_content_pages_detail_article(self, response):
        dict_result = from_string_to_json(response.text.encode('utf-8'))
        content_pages = dict_result['data']['list']
        content_page = response.meta
        for single_content_page in content_pages:
            single_content_page_dict = {}
            single_content_page_dict['logtime'] = int(single_content_page['event_day'])
            single_content_page_dict['readCount'] = int(single_content_page['view_count'])
            single_content_page_dict['shareCount'] = int(single_content_page['share_count'])
            single_content_page_dict['pvCount'] = int(single_content_page['recommend_count'])
            single_content_page_dict['likeCount'] = int(single_content_page['likes_count'])
            single_content_page_dict['commentCount'] = int(single_content_page['comment_count'])
            single_content_page_dict['collectCount'] = int(single_content_page['collect_count'])
            content_page['data']['dailies'].append(single_content_page_dict)
