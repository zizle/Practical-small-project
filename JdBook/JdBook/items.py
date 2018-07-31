# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 大分类的名字:
    big_name = scrapy.Field()

    # 小分类的名字
    small_name = scrapy.Field()
    # 小分类的url
    small_link = scrapy.Field()

    book_img_url = scrapy.Field()
    # 图书的名字
    book_name = scrapy.Field()
    # 图书的作者
    book_author = scrapy.Field()

    # 出版社
    book_store = scrapy.Field()

    # 出版时间
    book_time = scrapy.Field()

    # 商品id
    book_sku_id = scrapy.Field()

    # 商品价格
    book_price = scrapy.Field()
