# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    work_name = scrapy.Field()
    publish_date = scrapy.Field()
    post_type = scrapy.Field()
    work_place = scrapy.Field()
    recruit_num = scrapy.Field()
    service_condition = scrapy.Field()
