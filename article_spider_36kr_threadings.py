# _*_ coding:utf-8 _*_

# _*_ coding:utf-8 _*_

# 获取36kr网站的文章
import requests
import json
import jsonpath
import re
import threading


class ThreeSixSpider(object):
    _collect_url = []

    def __init__(self):
        # ?per_page=20&page=
        self.url_dict = {
            'technology': 'http://36kr.com/api/search-column/218',
            'company': 'http://36kr.com/api/search-column/23',
            'consume': 'http://36kr.com/api/search-column/221',
            'entertainment': 'http://36kr.com/api/search-column/225',
            'education': 'http://36kr.com/api/search-column/227',
            'traffic': 'http://36kr.com/api/search-column/219',
            'skills': 'http://36kr.com/api/search-column/103'
        }
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.pattern = re.compile(r'<script>var props=(.*),locationnal=')

    def get_article(self, id, file_name):
        """获取数据"""
        print('开始获取'+ file_name + '的id为' + str(id) + '的文章...')
        # http://36kr.com/p/546210.html
        article_url = 'http://36kr.com/p/' + str(id) + '.html'
        response = requests.get(url=article_url, headers=self.headers)
        if response.status_code != 200:
            self._collect_url.append(article_url)
            with open('36kr/url.txt', 'w', encoding='utf-8') as f:
                f.write(str(self._collect_url))
                print('请求数据错误...')
            return
        article_data = response.content.decode()
        # 正则匹配
        re_data = self.pattern.findall(article_data)
        finally_data = json.loads(re_data[0])
        article_content = jsonpath.jsonpath(finally_data, '$..content')
        article_summary = jsonpath.jsonpath(finally_data, '$..summary')
        article_title = jsonpath.jsonpath(finally_data, '$..title')
        article_cover = jsonpath.jsonpath(finally_data, '$..cover')
        title = article_title[0]
        summary = article_summary[0]
        cover = article_cover[0]
        content = article_content[0]
        # 写入文件
        self.save_file(file_name, title, summary, cover, content)
        print('获取' + file_name + '的id为:' + str(id) + '的文章成功!')

    @staticmethod
    def save_file(file_name, title, summary, cover, content):
        """写入文件"""

        with open('36kr/'+file_name + '.txt', 'a', encoding='utf-8') as f:
            data = '标题：' + title + '\n' + '\t摘要:' + summary + '\n' + '\t插图url:' + cover + '\n内容:' + content + '\n\n'
            f.write(data)

    def get_pages(self, url):
        """获取页数"""
        # 'http://36kr.com/api/search-column/218'
        response_data = requests.get(url=url, headers=self.headers).content.decode()
        response_dict = json.loads(response_data)
        # 解析数据
        total_count = response_dict['data']['total_count']
        page_size = response_dict['data']['page_size']
        pages = (total_count // int(page_size)) + 1
        return pages

    def article_ids(self, url):
        # 'http://36kr.com/api/search-column/218?per_page=10&page=1'
        """获取当前分类的文章id类表"""
        response_data = requests.get(url=url, headers=self.headers).content.decode()
        response_dict = json.loads(response_data)
        items_list = response_dict['data']['items']
        id_list = []
        for item in items_list:
            id_list.append(item['id'])
        return id_list

    def task(self, url, url_key):
        """多线程任务"""
        # 获取页数
        pages = self.get_pages(url)
        # 获取文章的id列表
        article_id_list = []
        for page in range(1, pages + 1):
            print('抓取第' + str(page) + '页的文章id...')
            ids_url = url + '?per_page=10&page=' + str(page)
            id_list = self.article_ids(ids_url)
            article_id_list.extend(id_list)
            print('第' + str(page) + '页的文章id抓取完毕!')
        # 获取文章
        print('开始抓取' + url_key + '的数据...')
        for id in article_id_list:
            self.get_article(id, url_key)
        print('抓取' + url_key + '的数据结束!')


    def run(self):
        """产生url,并发送请求"""
        for url_key, url in self.url_dict.items():
            f = open('36kr/' + url_key + '.txt', 'w', encoding='utf-8')
            f.close()

            # 开启多线程，每一个文章类一个线程去执行
            t = threading.Thread(target=self.task, args=(url, url_key))
            t.start()
            print('当前运行的线程数为: %d' % len(threading.enumerate()))

            # # 获取页数
            # pages = self.get_pages(url)
            # # 获取文章的id列表
            # article_id_list = []
            # for page in range(1, pages+1):
            #     print('抓取第' + str(page) +'页的文章id...')
            #     ids_url = url + '?per_page=10&page=' + str(page)
            #     id_list = self.article_ids(ids_url)
            #     article_id_list.extend(id_list)
            #     print('第'+str(page) + '页的文章id抓取完毕!')
            # # 获取文章
            # print('开始抓取' + url_key + '的数据...')
            # for id in article_id_list:
            #     self.get_article(id, url_key)
            # print('抓取' + url_key + '的数据结束!')


if __name__ == '__main__':
    three_six_spider = ThreeSixSpider()
    three_six_spider.run()
