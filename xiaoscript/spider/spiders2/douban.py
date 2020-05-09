#!/usr/bin/env python
# encoding: utf-8

"""
@description: 豆瓣小组爬虫

@author: baoqiang
@time: 2019-09-24 21:12
"""
import random
import sys

from xiaoscript import config
from threading import Lock
import scrapy
from scrapy.http import FormRequest
import json
import re

start_url = 'https://www.douban.com/group/513717/discussion?start={}'

id_pat = re.compile('https://www.douban.com/group/topic/([\\d]+)')

out_file = '{}/douban_xiaozu.json'.format(config.get_root_path())


class DoubanXiaozuSpider(scrapy.Spider):
    name = 'douban_xiaozu_spider'

    lock = Lock()
    ids = set()

    def start_requests(self):
        # for i in range(0, 731):
        for i in range(0, 100):
            url = start_url.format(i * 25)
            headers.update({'X-Real-IP': get_random_ip()})
            yield FormRequest(url, headers=headers, callback=self.parse_cate)

    def parse_cate(self, response):
        # if response.status_code != 200:
        #     sys.exit(-1)

        classes = response.selector.xpath(
            './/div[@class="article"]//table/tr[@class!="th"]')

        datas = []

        for item in classes:
            dic = {'from_url': response.url}

            title_url = item.xpath('.//td[@class="title"]/a')
            dic['url'] = title_url.xpath('./@href')[0].extract().strip()
            dic['title'] = title_url.xpath('./@title')[0].extract().strip()

            user_url = item.xpath('.//td')[1]
            if user_url and user_url.xpath('.//text()'):
                dic['name'] = user_url.xpath('.//text()')[0].extract().strip()
            else:
                dic['name'] = ''

            time_url = item.xpath('.//td[@class="time"]')
            dic['time'] = time_url.xpath('./text()')[0].extract().strip()

            dic['id'] = parse_id(dic['url'])

            # add one
            if not dic['id'] in self.ids:
                datas.append(dic)
                self.ids.add(dic['id'])

        self.write_file(datas)

    def write_file(self, results):
        self.lock.acquire()

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

        self.lock.release()


def get_random_ip():
    return '.'.join(
        [str(int(''.join([str(random.randint(0, 2)), str(random.randint(0, 5)), str(random.randint(0, 5))]))) for _ in
         range(4)])


def parse_id(url):
    m = id_pat.match(url)
    if m:
        return m.group(1)
    else:
        return 0


headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13E234 MicroMessenger/6.5.20 NetType/WIFI Language/zh_CN'
}

if __name__ == '__main__':
    pass
