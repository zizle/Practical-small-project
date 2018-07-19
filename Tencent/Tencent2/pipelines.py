# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from .items import Tencent2Item


class Tencent2Pipeline(object):
    def open_spider(self, spider):
        self.file = open('tencent.json', 'w')
        self.file.write('[')

    def process_item(self, item, spider):
        if isinstance(item, Tencent2Item):
            # 转化为字典
            dict_data = dict(item)
            # 转为json
            json_data = json.dumps(dict_data) + ',\n'
            # 写入文件
            self.file.write(json_data)

        return item

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()
