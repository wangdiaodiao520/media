# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

import datetime

from collections import defaultdict

import six
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse, Response
from scrapy.http.cookies import CookieJar
from selenium import webdriver

from media_spider.middlewares_manager.download_middlewares import get_qi_e_response, get_qq_kandian_response, \
    get_bai_jia_response, get_dayu_response, get_yidian_response
from media_spider.spiders.baijia_spider import BaiJiaSpider
from media_spider.spiders.dayu_spider import DaYuSpider
from media_spider.spiders.qier_spider import QiESpider
from media_spider.spiders.qq_kandian_spider import QQKanDianSpider
from media_spider.spiders.yidian_spider import YiDianSpider


class MediaSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MediaSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        # self.driver = webdriver.Chrome()
        pass

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if isinstance(spider, QiESpider):
            response = get_qi_e_response(spider,request)
        elif isinstance(spider, QQKanDianSpider):
            response = get_qq_kandian_response(spider, request)
        elif isinstance(spider, BaiJiaSpider):
            response = get_bai_jia_response(spider, request)
        elif isinstance(spider, DaYuSpider):
            response = get_dayu_response(spider, request)
        elif isinstance(spider, YiDianSpider):
            response = get_yidian_response(spider, request)
        return response

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CookiesMiddleware(object):
    """
    中间件在Scrapy启动时实例化.其中jars属性是一个默认值为CookieJar对象的dict.
    该中间件追踪web server发送的cookie,保存在jars中,并在之后的request中发送回去,
    类似浏览器的行为.

    CookiesMiddleware还用于实现单Spider多cookie.通过在Request meta中添加cookiejar来支持单
    spider追踪多cookie session.默认情况下其使用一个cookie jar(session)，不过您可以传递一个
    标示符来使用多个。
    例如:
    for i, url in enumerate(urls):
        yield scrapy.Request("http://www.example.com", meta={'cookiejar': i},callback=self.parse_page)
    注意:meta中的cookiejar仅存储了cookiejar的标识,真是的cookiejar存储在CookiesMiddleware实
    例的jars属性中
    """
    def __init__(self, debug=False):
        self.jars = defaultdict(CookieJar)
        self.debug = debug

    @classmethod
    def from_crawler(cls, crawler):
        # COOKIES_ENABLED默认值为True,是否启用CookiesMiddleware
        # COOKIES_DEBUG默认值为False,如果启用，Scrapy将记录所有在request(Cookie 请求头)发
        # 送的cookies及response接收到的cookies(Set-Cookie 接收头)。
        if not crawler.settings.getbool('COOKIES_ENABLED'):
            raise NotConfigured
        return cls(crawler.settings.getbool('COOKIES_DEBUG'))

    def process_request(self, request, spider):
        if request.meta.get('dont_merge_cookies', False):
            return
        # 如果在request meta中使用了cookiejar, cookiejarkey为对应的标识.
        # 否则cookiejarkey为None
        cookiejarkey = request.meta.get("cookiejar")
        # 第一次执行jars会为每个key产生一个默认值cookiejar对象.默认为{None: cookiejar}
        jar = self.jars[cookiejarkey]
       # 见下面_get_request_cookies()方法
        cookies = self._get_request_cookies(jar, request)
        for cookie in cookies:
            jar.set_cookie_if_ok(cookie, request)
        # set Cookie header
        request.headers.pop('Cookie', None)
        # 将cookie加入到request的headers中
        jar.add_cookie_header(request)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_merge_cookies', False):
            return response
        # extract cookies from Set-Cookie and drop invalid/expired cookies
        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]
       # 在请求允许的情况下(?),从response中提取cookie并入当前的cookiejar
        jar.extract_cookies(response, request)
        self._debug_set_cookie(response, spider)

        return response

    def _format_cookie(self, cookie):
        # 对以字典或字典的列表的形式传入的cookie进行格式化
        cookie_str = '%s=%s' % (cookie['name'], cookie['value'])

        if cookie.get('path', None):
            cookie_str += '; Path=%s' % cookie['path']
        if cookie.get('domain', None):
            cookie_str += '; Domain=%s' % cookie['domain']

        return cookie_str

    def _get_request_cookies(self, jar, request):
        # 将request中cookies参数添加的cookie合并到当前的cookiejar中
        if isinstance(request.cookies, dict):
            cookie_list = [{'name': k, 'value': v} for k, v in \
                    six.iteritems(request.cookies)]
        else:
            cookie_list = request.cookies

        cookies = [self._format_cookie(x) for x in cookie_list]
        headers = {'Set-Cookie': cookies}
        # 使用刚才获取的cookie构造一个响应对象
        response = Response(request.url, headers=headers)
        # cookiejar.make_cookies方法从response中提取cookie放入当前cookiejar中.
        return jar.make_cookies(response, request)
