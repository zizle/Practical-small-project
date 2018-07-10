# _*_ coding:utf-8 _*_

# 爬取内涵吧段子
import requests
import re


class NeiHanSpider(object):
    """
    内涵吧段子里的内涵段子爬虫
    """

    def __init__(self):
        self.base_url = 'https://www.neihan8.com/article/list_5_'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

        # 匹配页数正则对象
        # <span class="pageinfo">共 <strong>(\d+)</strong>页
        self.page_pattern = re.compile(r'<span class="pageinfo">共 <strong>(\d+)</strong>页')

        # 初步解析的正则对象
        # <div class="f18 mb20">(.*?)</div>
        self.general_pattern = re.compile(r'<div class="f18 mb20">(.*?)</div>', re.S)

        # 深度解析正则对象
        self.depth_pattern = re.compile(r'<.*?>|&.*?;|\s')

    def send_request(self, url):
        """发送请求"""
        response = requests.get(url=url, headers=self.headers)
        response_data = response.content.decode(encoding='gbk')
        return response_data

    def extract_pages(self):
        """提取页码"""
        url = self.base_url + "1.html"
        response = requests.get(url=url, headers=self.headers)
        response_data = response.content.decode(encoding='gbk')
        return int(self.page_pattern.search(response_data).group(1))

    def analysis_data(self, data):
        """解析数据"""
        # 初步解析
        extract_datas = self.general_pattern.findall(data)
        # 深度解析
        depth_datas = []
        for extract_data in extract_datas:
            # 深度解析
            depth_data = self.depth_pattern.sub('', extract_data)
            depth_datas.append(depth_data)
        return depth_datas

    @staticmethod
    def save_data(page, data):
        """保存文件"""
        print('开始写入第{}页。。。'.format(page))
        with open('download_neihanba.txt', 'a', encoding='utf-8') as f:
            page_data = '--------------------第' + str(page) + '页--------------------\n\n'
            f.write(page_data)
            for index, content in enumerate(data):
                row_data = str(index + 1) + ':\t' + content + '。\n\n'
                f.write(row_data)
        print('第{}页写入完成!'.format(page))

    def generate_urls(self, total_page):
        """生成url列表"""
        url_list = []
        for page in range(1, total_page+1):
            url = self.base_url + str(page) + '.html'
            url_list.append(url)
        return url_list

    def run(self):
        """方法调度"""
        # 请求获取总页码
        total_page = self.extract_pages()
        # 获取url列表
        url_list = self.generate_urls(total_page)
        for index, url in enumerate(url_list):
            # 发送请求
            data = self.send_request(url)
            # 提取数据
            finally_data = self.analysis_data(data)
            self.save_data(index+1, finally_data)


if __name__ == '__main__':
    spider = NeiHanSpider()
    spider.run()


