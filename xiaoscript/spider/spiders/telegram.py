#!/usr/bin/env python
# encoding: utf-8


"""
@description: telegram 爬取数据群组的关注的人数

@author: pacman
@time: 2018/3/20 16:25
"""

import scrapy
from scrapy import Request
import json
import re

start_url = 'https://0924.tk/2017/10/02/Telegram-Group%E3%80%81Channel%E3%80%81Bot-share/'
start_url2 = 'http://90fuli.com/?p=245'

root_file = 'C:\\Users\\xiaobao\\Desktop\\telegram.json'
root_file2 = 'C:\\Users\\xiaobao\\Desktop\\telegram.txt'


class TelegramSpider(scrapy.Spider):
    name = 'telegram'

    def start_requests(self):
        # yield Request(start_url, callback=self.parse_list)
        yield Request(start_url2, callback=self.parse_list2)

    def parse_list(self, response):
        classes = response.selector.xpath('//div[@class="post-body"]/ul/li/ul/li/a')
        for item in classes:
            url = item.xpath('./@href')[0].extract().strip()

            if not is_telegram_url(url):
                continue

            yield Request(url, callback=self.parse_item)

    def parse_list2(self, response):
        classes = response.selector.xpath('//div[@class="entry-content"]/ul/li/ul/li')
        for item in classes:
            text = item.xpath('./text()')[0].extract().strip()

            pat = re.compile('https://t.*')
            m = pat.search(text)
            url = m.group() if m else ''

            if not is_telegram_url(url):
                continue

            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        dic = {}

        tgme = response.selector.xpath('.//div[contains(@class,"tgme_page")]')

        dic['title'] = tgme.xpath('.//div[@class="tgme_page_title"]//text()')[0].extract().strip()
        desc = tgme.xpath('.//div[@class="tgme_page_description"]//text()')
        dic['desc'] = desc[0].extract().strip() if desc else ''

        num_str = tgme.xpath('.//div[@class="tgme_page_extra"]//text()')[0].extract().strip()
        dic['num'] = trim(num_str)
        dic['url'] = response.url

        with open(root_file, 'a', encoding='utf-8') as fw:
            json.dump(dic, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')


def trim(num_str):
    try:
        return int(num_str.replace(' ', '').replace('members', '').strip())
    except:
        print(num_str)
        return 0


def is_telegram_url(url):
    if 'telegram' in url:
        return True
    if 't.me' in url:
        return True
    return False


def process():
    with open(root_file, 'r', encoding='utf-8') as f, \
            open(root_file2, 'w', encoding='utf-8') as fw:
        for line in f:
            jdata = json.loads(line.strip())
            fw.write('{}\t{}\t{}\t{}\n'.format(jdata['url'], jdata['title'], jdata['num'], jdata['desc']))


def main():
    process()


if __name__ == '__main__':
    main()
