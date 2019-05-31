#!/usr/bin/env python
# encoding: utf-8

"""
@description: 获取简书的collection

@author: baoqiang
@time: 2019-05-31 20:07
"""

import scrapy
from scrapy import Request
from threading import Lock
import json
from xiaoscript import config
import time
import random

start_url = 'https://www.jianshu.com/recommendations/collections?page={}&order_by=hot'
root_url = 'https://www.jianshu.com'

out_file = '{}/jianshu.json'.format(config.get_root_path())


class JianshuSpider(scrapy.Spider):
    name = 'jianshu_collection'

    lock = Lock()

    def start_requests(self):
        # for i in range(1, 3):
        for i in range(1, 40):
            url = start_url.format(i)
            yield Request(url, callback=self.parse_page)

            time.sleep(random.random())

    def parse(self, response):
        pass

    def parse_page(self, response):
        classes = response.selector.xpath('.//div[@id="list-container"]/div')

        datas = []
        for item in classes:
            dic = {'from_url': response.url}

            # col part
            col_part = item.xpath('.//div[@class="collection-wrap"]')

            url = col_part.xpath('./a/@href')[0].extract().strip()
            dic['url'] = '{}{}'.format(root_url, url)

            name = col_part.xpath('.//h4/text()')[0].extract().strip()
            dic['name'] = name

            desc = col_part.xpath('.//p/text()')
            if desc:
                dic['desc'] = desc[0].extract().strip()
            else:
                dic['desc'] = ''

            # get id
            id_url = col_part.xpath('.//a[@class="follow-btn"]')
            id_str = id_url.xpath('./@props-data-collection-id')[0].extract().strip()
            dic['id'] = int(id_str)

            # count part
            count_part = item.xpath('.//div[@class="count"]')

            count_str = count_part.xpath('./a/text()')[0].extract().strip()
            dic['count'] = trim_count(count_str)

            follow_str = count_part.xpath('./text()')[0].extract().strip()
            dic['follow'] = trim_follow(follow_str)

            # print('dic: {}'.format(dic))

            datas.append(dic)

        self.write_file(datas)

    def write_file(self, results):
        self.lock.acquire()

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

        self.lock.release()


def trim_count(count_str):
    if not count_str:
        return 0

    return int(count_str.replace('篇文章', ''))


def trim_follow(follow_str):
    if not follow_str:
        return 0

    follow_str = follow_str.replace('·', '').replace('人关注', '').strip()

    if 'K' in follow_str:
        follow_str = follow_str.replace('K', '')
        return int(float(follow_str) * 1000)
    else:
        return int(follow_str)


if __name__ == '__main__':
    pass
