# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class BaiduPipeline(object):
    def open_spider(self, spider):
        self.file = open('baidu.json', 'w')
        self.file.write('[')

    def process_item(self, item, spider):
        data_dict = dict(item)
        json_data = json.dumps(data_dict) + ',\n'
        self.file.write(json_data)
        return item

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()