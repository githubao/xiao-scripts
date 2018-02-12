#!/usr/bin/env python
# encoding: utf-8

"""
@description: 大众点评的爬虫，只要 位置 和 评论的数量 就好了

@author: pacman
@time: 2018/2/12 10:50
"""

import scrapy
from scrapy import Request
import json
import traceback

# outfile = 'C:\\Users\\xiaobao\\Desktop\\dianping.json'
outfile = '/mnt/home/baoqiang/dianping.json'


class DianpingSpider(scrapy.Spider):
    name = 'dianping'

    start_urls = []

    def start_requests(self):
        return [Request('http://www.dianping.com/beijing/ch10/o3', callback=self.parse_cate)]

    def parse_cate(self, response):
        classes = response.selector.xpath('//div[@id="metro-nav"]/a')
        for item in classes:
            url = item.xpath('./@href')[0].extract().strip()
            line = item.xpath('.//text()')[0].extract().strip()

            yield Request(url, callback=self.parse_metro, meta={'line': line})

            # break

    def parse_metro(self, response):
        classes = response.selector.xpath('//div[@id="metro-nav-sub"]/a[not(contains(@class,"cur"))]')
        for item in classes:
            url = item.xpath('./@href')[0].extract().strip()
            station = item.xpath('.//text()')[0].extract().strip()

            yield Request(url, callback=self.parse_page,
                          meta={'line': response.meta['line'], 'station': station})

            # break

    def parse_page(self, response):
        pg_num = get_pg_num(response)

        url = response.url

        for i in range(1, pg_num + 1):
            yield Request('{}p{}'.format(url, i), callback=self.parse_item, meta=response.meta)

            # break

    def parse_item(self, response):
        results = []

        classes = response.selector.xpath('//div[@class="content"]//div[@id="shop-all-list"]//ul/li')
        for item in classes:
            dic = {'line': response.meta['line'], 'station': response.meta['station']}

            try:
                aurl = item.xpath('.//div[@class="tit"]/a')
                dic['url'] = aurl.xpath('./@href')[0].extract().strip()
                dic['name'] = aurl.xpath('.//h4/text()')[0].extract().strip()

                commenturl = item.xpath('.//div[@class="comment"]//b')
                dic['comment_cnt'] = commenturl.xpath('.//text()')[0].extract().strip()
                dic['price'] = commenturl.xpath('.//text()')[1].extract().strip().replace('￥', '')

                tagurl = item.xpath('.//div[@class="tag-addr"]//span[@class="tag"]')
                dic['tag'] = tagurl.xpath('.//text()')[0].extract().strip() if tagurl else '_'

            except Exception as e:
                traceback.print_exc()

            results.append(dic)

        with open(outfile, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')


def get_pg_num(response):
    classes = response.selector.xpath('//div[@class="page"]/a')
    item = classes[-2]
    pg_num = item.xpath('./text()')[0].extract().strip()
    return int(pg_num)


def main():
    print('do sth')


if __name__ == '__main__':
    main()
