# -*- coding: utf-8 -*-
import scrapy
from Tencent2.items import Tencent2Item


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    base_url = 'https://hr.tencent.com/position.php?keywords=python&tid=0&lid=2175&start='
    urls = []
    for page in range(0, 6):
        url = base_url + str(page * 10)
        urls.append(url)
    start_urls = urls

    def parse(self, response):

        print("==========================================请求地址：", response.url)
        tr_list = response.xpath('//tr[@class="even"] | //tr[@class="odd"]')
        for tr in tr_list:
            item = Tencent2Item()
            # 职位名称
            item['work_name'] = tr.xpath('./td[1]/a/text()').extract_first()
            # 职位类别
            item['work_type'] = tr.xpath('./td[2]/text()').extract_first()
            # 人数
            item['work_count'] = tr.xpath('./td[3]/text()').extract_first()
            # 地点
            item['work_place'] = tr.xpath('./td[4]/text()').extract_first()
            # 发布时间
            item['release_time'] = tr.xpath('./td[5]/text()').extract_first()
            # 连接地址
            item['link_url'] = 'https://hr.tencent.com/' + tr.xpath('./td[1]/a/@href').extract_first()

            # 发送详情页请求
            # request对象--引擎--调度器--出队列--引擎--下载器--response--引擎--爬虫--解析--request+item
            yield scrapy.Request(item['link_url'], meta={"item": item}, callback=self.details_parse)

    def details_parse(self, response):
        """解析详情页数据"""
        ul_list = response.xpath('//ul[@class="squareli"]')
        # 创建详情item对象
        item = response.meta.get('item')
        item['work_duty'] = ''.join(ul_list[0].xpath('./li/text()').extract())
        item['work_require'] = ''.join(ul_list[1].xpath('./li/text()').extract())
        yield item



