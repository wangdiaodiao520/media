# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from media_spider.dao.dao_url_post import post_item


class MediaSpiderPipeline(object):
    def process_item(self, item, spider):
        post_item(item)