# -*- coding: utf-8 -*-
import scrapy
import json

from Baidu.items import BaiduItem


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    base_url = 'https://talent.baidu.com/baidu/web/httpservice/getPostList?postType=&workPlace=0/4/7/9&recruitType=2&keyWord=python&pageSize=10&curPage='
    cur_page = 1
    start_urls =[base_url + str(cur_page)]

    def parse(self, response):
        """解析数据"""
        print('请求地址=========================================:', response.url)
        datas = json.loads(response.body_as_unicode())
        data_list = datas['postList']

        # 总页数
        total_page = datas['totalPage']

        for data in data_list:
            item = BaiduItem()
            item['work_name'] = data['name']
            item['publish_date'] = data['publishDate']
            item['post_type'] = data['postType']
            item['work_place'] = data['workPlace']
            item['recruit_num'] = data['recruitNum']
            item['service_condition'] = data['serviceCondition']
            yield item

        self.cur_page += 1
        if self.cur_page <= total_page:
            url = self.base_url + str(self.cur_page)
            yield scrapy.Request(url=url, callback=self.parse)




