#!/usr/bin/env python
# encoding: utf-8

"""
@description: go语言网爬虫

@author: baoqiang
@time: 2018/11/6 下午4:35
"""

import scrapy
from scrapy.http import FormRequest
import json
from xiaoscript.config import get_root_path

out_file = '{}/study_go.json'.format(get_root_path())
url_fmt = 'https://studygolang.com/articles?p={}'
root_url = 'https://studygolang.com'


class StudyGoSpider(scrapy.Spider):
    name = 'studygo'

    def start_requests(self):
        for i in range(1, 798):
        # for i in range(1, 3):
            url = url_fmt.format(i)
            yield FormRequest(url, callback=self.parse_cate)

    def parse_cate(self, response):
        datas = []

        classes = response.selector.xpath('.//div[@class="container"]//article')
        for item in classes:
            dic = {"from_url": response.request.url}

            title_url = item.xpath('.//h2/a')
            dic['title'] = title_url.xpath('./@title')[0].extract().strip()
            href = title_url.xpath('./@href')[0].extract().strip()
            dic['url'] = root_url + href
            dic['id'] = int(href.replace('/articles/', ''))

            meta_url = item.xpath('.//div[contains(@class,"metatag")]')
            dic['date'] = meta_url.xpath('.//span[@class="date"]/text()')[0].extract().strip()
            tags_url = meta_url.xpath('.//ul[@class="list-inline"]/li//text()')
            dic['tags'] = [item.extract().strip() for item in tags_url if item.extract().strip()]
            dic['read'] = int(meta_url.xpath('./span[@class="view"]/span/text()')[0].extract().strip())

            datas.append(dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in datas:
                json.dump(item, fw, ensure_ascii=False)
                fw.write('\n')
