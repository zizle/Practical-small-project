# -*- coding: utf-8 -*-
import scrapy
from JdBook.items import JdbookItem
import json
from copy import deepcopy


class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']
    page = 0

    def parse(self, response):
        dt_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt')
        for dt in dt_list:
            item = JdbookItem()
            # 大类名称
            item['big_name'] = dt.xpath('./a/text()').extract_first()
            # 小类名称和url
            em_list = dt.xpath('./following-sibling::*[1]/em')
            for em in em_list[:1]:
                item['small_name'] = em.xpath('./a/text()').extract_first()
                item['small_link'] = 'https:' + em.xpath('./a/@href').extract_first()
                # 发送小类的请求
                yield scrapy.Request(
                    url=item['small_link'],
                    callback=self.parse_book_list,
                    meta={'book': deepcopy(item)}
                )

    def parse_book_list(self, response):
        item = response.meta['book']
        li_list = response.xpath('//*[@id="plist"]/ul/li')
        for li in li_list:
            # 书的图片link
            item['book_img_url'] = 'https:' + li.xpath('.//div[@class="p-img"]/a/img/@src').extract_first()
            # 书的名字
            item['book_name'] = li.xpath('.//div[@class="p-name"]/a/em/text()').extract_first().strip()
            # 作者
            item['book_author'] = li.xpath('.//span[@class="p-bi-name"]/span/a/text()').extract_first()
            # 出版社
            item['book_store'] = li.xpath('.//span[@class="p-bi-store"]/a/text()').extract_first()
            # 出版时间
            item['book_time'] = li.xpath('.//span[@class="p-bi-date"]/text()').extract_first().strip()
            item['book_sku_id'] = li.xpath('./div/@data-sku').extract_first()
            # 价格
            # https://p.3.cn/prices/mgets?&ext=11000000&pin=&type=1&area=1_72_4137_0&skuIds=J_11757834
            price_url = 'https://p.3.cn/prices/mgets?&ext=11000000&pin=&type=1&area=1_72_4137_0&skuIds=J_{}'.format(item['book_sku_id'])
            # 发送价格请求
            yield scrapy.Request(
                url=price_url,
                callback=self.parse_price,
                meta={'book': deepcopy(item)}
            )


        # 翻页
        next_url = response.xpath('//*[@id="J_bottomPage"]/span[1]/a[10]/@href').extract_first()
        self.page += 1
        if next_url is not None:
            if self.page > 3:
                return
            yield response.follow(
                next_url,
                callback=self.parse_book_list,
                meta={'book': item}
            )

    def parse_price(self, response):
        """解析价格"""
        item = response.meta['book']
        item['book_price'] = json.loads(response.body.decode())[0]['p']
        yield item






