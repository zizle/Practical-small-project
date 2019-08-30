import requests
import time
from lxml import etree

main_url = 'https://www.2wxs.com'

fail_list = list()


def get_html(url):
    try:
        response = requests.get(
            url=url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            }
        )
    except Exception as e:
        fail_list.append(url)
        return
    if response.status_code != 200:
        fail_list.append(url)
        return
    content = response.content.decode('gbk')
    # print(content)
    html = etree.HTML(content)
    inner = html.xpath('//div[@class="inner"]')[0]
    title = inner.xpath('.//h1/text()')[0].strip(' ')
    pages = inner.xpath('.//div[@class="link"]/a')
    next_page_url = None
    for page_e in pages:
        if page_e.xpath('text()')[0] == '下一页':
            next_page_url = main_url + page_e.xpath('@href')[0]
            break

    book_text = inner.xpath('//div[@id="BookText"]/text()')
    # 遍历出每一段内容
    # print(title)
    # for each_block in book_text:
    #     print(each_block)
    if not all([title, book_text, next_page_url]):
        fail_list.append(url)
    # 写入失败的url
    with open('fail.txt', 'a') as f:
        f.write(';'.join(fail_list))
    return title, book_text, next_page_url


if __name__ == '__main__':
    next_page_url = 'https://www.2wxs.com/xstxt/312/118706.html'
    while True:
        time.sleep(2)
        if next_page_url:
            title, book_text, next_page_url = get_html(next_page_url)
            with open('book/斗罗大陆(全本).txt', 'a') as f:
                f.write(title)
                f.write('\r\n')
                f.write('\r\n')
                for each_block in book_text:
                    f.write(each_block)
                f.write('\r\n')
                f.write('\r\n')
                f.write('\r\n')
            print(title, '获取完成!')












