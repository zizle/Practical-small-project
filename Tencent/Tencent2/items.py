# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Tencent2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位名称
    work_name = scrapy.Field()
    # 职位类别
    work_type = scrapy.Field()
    # 人数
    work_count = scrapy.Field()
    # 地点
    work_place = scrapy.Field()
    # 发布时间
    release_time = scrapy.Field()
    # 连接地址
    link_url = scrapy.Field()

    work_duty = scrapy.Field()
    work_require = scrapy.Field()

