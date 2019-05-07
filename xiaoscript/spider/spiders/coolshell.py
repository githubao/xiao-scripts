#!/usr/bin/env python
# encoding: utf-8

"""
@description: 酷壳爬虫

@author: baoqiang
@time: 2019-04-23 12:35
"""

import json
import re
import urllib.parse
import logging
import threading

import scrapy
from scrapy import Request

from xiaoscript import config

start_url = 'https://coolshell.cn/page/{}'

out_file = '{}/coolshell.json'.format(config.get_root_path())

id_pat = re.compile('https://coolshell.cn/articles/(\d+).html')


class CollShellSpider(scrapy.Spider):
    name = 'cool_shell'

    lock = threading.Lock()

    def start_requests(self):
        for i in range(1, 72):
        # for i in range(1, 3):
            url = start_url.format(i)
            yield Request(url, callback=self.parse_page)

    def parse(self, response):
        pass

    def parse_page(self, response):
        datas = []
        classes = response.selector.xpath('.//div[@id="primary"]//article')
        for item in classes:
            dic = {}

            title_url = item.xpath('.//h2[@class="entry-title"]/a')
            dic['title'] = title_url.xpath('./text()')[0].extract().strip()
            dic['url'] = title_url.xpath('./@href')[0].extract().strip()
            dic['id'] = parse_id(dic['url'])

            time_url = item.xpath('.//time[@class="entry-date"]')
            dic['time'] = time_url.xpath('./text()')[0].extract().strip()

            comment_url = item.xpath('.//a[@class="comments-link"]')
            comment_text = comment_url.xpath('./text()')[0].extract().strip()
            dic['comment_count'] = trim_comment(comment_text)

            read_url = item.xpath('.//h5[@class="entry-date"]')
            read_text = ''.join(i.extract().strip() for i in read_url.xpath('./text()'))
            dic['read_count'] = trim_read(read_text)

            rate_url = item.xpath('.//div[@class="post-ratings"]')
            rate_count = int(rate_url.xpath('./strong/text()')[0].extract().strip())
            dic['rate_count'] = rate_count

            rate_avg = float(rate_url.xpath('./strong/text()')[1].extract().strip())
            dic['rate_avg'] = rate_avg

            datas.append(dic)

        self.write_file(datas)

    def write_file(self, results):
        self.lock.acquire()

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

        self.lock.release()


def parse_id(url):
    m = id_pat.match(url)
    if m:
        return m.group(1)

    return 0


def trim_comment(text):
    text = text.replace(' 条评论', '')
    text = text.replace(',', '')
    text = text.replace('没有评论', '')
    text = text.replace(' ', '')
    return int(text) if text else 0


def trim_read(text):
    text = text.replace(' 人阅读', '')
    text = text.replace(',', '')
    return int(text)


if __name__ == '__main__':
    pass
