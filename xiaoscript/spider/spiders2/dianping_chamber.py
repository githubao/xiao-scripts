#!/usr/bin/env python
# encoding: utf-8

"""
@description: 大众点评 北京密室

@author: baoqiang
@time: 2019-06-30 12:52
"""

import scrapy
from scrapy import FormRequest
from threading import Lock
import json
from xiaoscript import config

url_fmt = 'http://www.dianping.com/beijing/ch30/g2754p{}'

out_file = '{}/chamber.json'.format(config.get_root_path())


class DianpingChamberSpider(scrapy.Spider):
    name = 'dianping_chamber'

    lock = Lock()

    def start_requests(self):
        for i in range(1, 24):
            url = url_fmt.format(i)
            yield FormRequest(url, callback=self.parse_page, headers=headers)

    def parse_page(self, response):
        classes = response.selector.xpath('.//div[@class="content"]//ul/li')

        datas = []
        for item in classes:
            dic = {'from_url': response.url}

            txt_url = item.xpath('./div[@class="txt"]')

            if not txt_url:
                continue

            a_url = txt_url.xpath('./div[@class="tit"]/a')
            dic['title'] = a_url.xpath('./@title')[0].extract().strip()
            dic['url'] = a_url.xpath('./@href')[0].extract().strip()

            datas.append(dic)

        self.write_file(datas)

    def write_file(self, results):
        self.lock.acquire()

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

        self.lock.release()


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie': 'copy from browser',
    'Referer': 'http://www.dianping.com/beijing/ch30/g2754p3'
}

if __name__ == '__main__':
    pass
