# _*_ coding:utf-8 _*_
# 可以下载付费音乐的下载器, 不过就是比较麻烦, 要从源网页试听, 检查其网页源代码
# 提取出含有.mp3的url地址
import re


def get_music_url():
    src_url = input('请输入含有.mp3的URl地址:')
    # 用正则匹配出url地址
    match = re.match(r'.*(http://.*\.mp3).*', src_url)
    if match:
        music_url = match.group(1)
        print('找到音乐的资源路径:{}'.format(music_url))
        return music_url
    else:
        print('输入的地址有误！')


if __name__ == '__main__':
    music_name = input('请输入您要生成的文件名:')
    get_music_url()
