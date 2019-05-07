#!/usr/bin/env python
# encoding: utf-8

"""
@description: 北京景点爬虫

@author: baoqiang
@time: 2019-05-07 20:50
"""

import scrapy
from scrapy import Request
from xiaoscript import config
import json

page_size = 30
url_fmt = 'https://www.tripadvisor.com.hk/Attractions-g294212-Activities-oa{}-Beijing.html'
out_file = '{}/bj_tour.json'.format(config.get_root_path())


class TripAdvisorSpider(scrapy.Spider):
    name = 'trip_advisor'

    def start_requests(self):
        for i in range(0, 55):
            # for i in range(1, 2):
            url = url_fmt.format(page_size * i)

            yield Request(url, callback=self.parse_page, meta={'page': i})

    def parse_page(self, response):
        meta = response.meta

        classes = response.selector.xpath('.//div[@class="listing_info"]')

        results = []
        for idx, item in enumerate(classes, start=1):
            dic = {}
            dic['rank'] = meta['page'] * page_size + idx

            tag_url = item.xpath('.//div[@class="tag_line"]//span/text()')
            if tag_url:
                dic['tag'] = tag_url[0].extract().strip()
            else:
                dic['tag'] = "-"

            title_url = item.xpath('.//div[contains(@class,"listing_title")]/a/text()')
            dic['title'] = title_url[0].extract().strip()

            results.append(dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')


if __name__ == '__main__':
    pass
