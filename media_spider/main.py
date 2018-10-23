#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
# process.crawl('qi_e_spider')
# process.crawl('qq_kandian_spider')
# process.crawl('bai_jia_spider')
process.crawl('dayu_spider')
# process.crawl('yidian_spider')
process.start()


# cmdline.execute("scrapy crawl qi_e_spider".split())
# cmdline.execute("scrapy crawl yi_dian_spider".split())
# cmdline.execute("scrapy crawl demo_spider".split())
# cmdline.execute("scrapy crawl qq_kandian_spider".split())

