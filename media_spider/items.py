# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MediaSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CommonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index_pages = scrapy.Field()
    user_pages = scrapy.Field()
    income_pages = scrapy.Field()
    content_pages = scrapy.Field()
    account = scrapy.Field()