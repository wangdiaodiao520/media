#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

__author__ = 'zengyang@tv365.net(ZengYang)'

process = CrawlerProcess(get_project_settings())
process.crawl('qq_kandian_spider')
process.start()



