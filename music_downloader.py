# _*_ coding:utf-8 _*_
# 可以下载付费音乐的下载器, 不过就是比较麻烦, 要从源网页试听, 检查其网页源代码
# 提取出含有.mp3的url地址
import re
from urllib import request


def get_music_url():
    """获取音乐url"""
    src_url = input('请输入含有.mp3的URl地址:')
    # 用正则匹配出url地址
    match = re.match(r'.*(http://.*\.mp3).*', src_url)
    if match:
        music_url = match.group(1)
        print('找到音乐的资源路径:{}'.format(music_url))
        return music_url
    else:
        print('输入的地址有误！')


def get_music_source(music_url):
    """获取音乐资源"""
    # 构造请求头, 这里简单地只模拟浏览器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    req = request.Request(music_url, headers=headers)
    # 获取音乐
    response = request.urlopen(req)
    music_data = response.read()
    return music_data


if __name__ == '__main__':
    music_name = input('请输入您要生成的文件名:')
    music_url = get_music_url()
    music_data = get_music_source(music_url)
