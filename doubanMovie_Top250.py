# _*_ coding:utf-8 _*_

import urllib.request
import re
import ssl

# 忽略https安全验证
ssl._create_default_https_context = ssl._create_unverified_context


class MovieTop(object):
    def __init__(self):
        # 起始页码的第一条数据下标
        self.start = 0
        self.param = '&filter='
        # 构造请求的User-Agent
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        # 存放图片URL
        self.image_url_list = []
        # 存放影片名称
        self.image_name_list = []

    def get_page(self):
        """抓取页面"""

        try:
            while self.start <= 225:
                # 请求路径
                url = 'https://movie.douban.com/top250?start=' + str(self.start)
                # 构造请求
                req = urllib.request.Request(url, headers=self.headers)
                # 模拟浏览器发送请求
                response = urllib.request.urlopen(req)
                # 解码响应的数据
                page = response.read().decode('utf-8')
                # print(page)
                page_num = (self.start + 25)//25
                print('正在抓取第{}页数据...'.format(page_num))

                # 正则匹配图片地址
                img_url = re.findall(r"https://img.*\.jpg", str(page))
                # 加入到图片URl列表
                self.image_url_list.extend(img_url)
                # 正则匹配图片的名字
                name = re.findall(r""".*alt="(.*)" src""", str(page))
                # 加入名称列表
                self.image_name_list.extend(name)

                # 数据下标加上25刚好下一页
                self.start += 25
            print("总图片链接有{}个".format(len(self.image_url_list)))

        except Exception as e:
            print('抓取失败，原因是{}..'.format(e))

    def download(self):
        """下载图片"""
        try:
            if self.image_url_list:
                # 遍历url列表
                for index, image_url in enumerate(self.image_url_list):
                    print("正在下载第{}张图片...".format(index + 1))
                    # 构造请求头
                    request = urllib.request.Request(image_url, headers=self.headers)
                    # 发送请求
                    response = urllib.request.urlopen(request)
                    # 构造图片的名字
                    image_name = "./image/" + str(index + 1) + "、" + str(self.image_name_list[index]) + ".jpg"
                    # 写入文件
                    with open(image_name, "wb") as image:
                        # 循环读取数据, 模拟大文件, 理论上图片可以一次性全部读完
                        while True:
                            image_data = response.read(1024)
                            if image_data:
                                image.write(image_data)
                            else:
                                break
                    print("第{}张图片下载完成...".format(index + 1))

        except Exception as e:
            print('图片下载失败, 原因是{}'.format(e))

        else:
            print('全部图片下载成功...')


if __name__ == '__main__':
    # 实例化对象
    move_spider = MovieTop()
    # 爬取网页数据并得到URL
    move_spider.get_page()
    # 将图片保存到本地
    move_spider.download()






