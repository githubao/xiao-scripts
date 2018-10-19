#!/usr/bin/env python
# encoding: utf-8

"""
@description: 蛋壳的爬虫

@author: baoqiang
@time: 2018/10/19 下午12:10
"""

import json
import re
import urllib.parse
import logging

import scrapy
from scrapy import Request

from xiaoscript import config

start_url = 'https://www.dankegongyu.com/room/bj'

out_file = '{}/danke.json'.format(config.get_root_path())

id_pat = re.compile('https://www.dankegongyu.com/room/([\d]+).html')


class DankeSpider(scrapy.Spider):
    name = 'danke'

    def start_requests(self):
        yield Request(start_url, callback=self.parse_area)

    def parse_area(self, response):
        filter_div = './/div[@class="filter_options"]/dl[contains(@class,"area")]/dd/div[@class="option_list"]/div[@class="area-ls-wp"]'
        classes = response.selector.xpath(filter_div)

        for item in classes:
            town = item.xpath('./a/text()')[0].extract().strip()
            subclasses = item.xpath('.//div[@class="sub_option_list"]/a')

            for subitem in subclasses:
                area = subitem.xpath('./text()')[0].extract().strip()
                url = subitem.xpath('./@href')[0].extract().strip()

                logging.info('process : {} {}'.format(town, area))

                yield Request(url, meta={'town': town, 'area': area}, callback=self.parse_page)

                # return

    def parse_page(self, response):
        town = response.meta['town']
        area = response.meta['area']

        classes = response.selector.xpath('.//div[@class="roomlist"]//div[@class="r_lbx"]')

        results = []
        for item in classes:
            dic = {'town': town, 'area': area, 'from_url': urllib.parse.unquote(response.url)}

            location_url = item.xpath('./div[@class="r_lbx_cen"]/div[@class="r_lbx_cena"]/a')
            dic['url'] = location_url.xpath('./@href')[0].extract().strip()
            dic['id'] = parse_id(dic['url'])

            location_str = location_url.xpath('./@title')[0].extract().strip()
            parse_location(location_str, dic)

            subway_url = item.xpath('./div[@class="r_lbx_cen"]/div[@class="r_lbx_cena"]/div[@class="r_lbx_cena"]')
            dic['subway'] = ''.join(i.extract().strip() for i in subway_url.xpath('./text()'))

            size_url = item.xpath('./div[@class="r_lbx_cen"]/div[@class="r_lbx_cenb"]')
            size_str = ''.join(i.extract().strip() for i in size_url.xpath('./text()'))
            parse_size(size_str, dic)

            price_url = item.xpath('./div[@class="r_lbx_money"]/div[@class="r_lbx_moneya"]')

            first_month_url = price_url.xpath('./div[@class="room_price"]/em')
            if first_month_url:
                price = first_month_url.xpath('./text()')[0].extract().strip()
                price = int(price.replace('¥', '').replace('／月', '').strip())
            else:
                price = price_url.xpath('./span/text()')[0].extract().strip()
            dic['price'] = price

            results.append(dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

        next_url = get_next(response)

        if next_url:
            yield Request(next_url, meta={'town': town, 'area': area}, callback=self.parse_page)


def parse_size(size_str, dic):
    sizes = size_str.split('|')
    dic['size'] = float(sizes[0].replace('建筑面积约', '').replace('㎡', '').strip())
    dic['floor'] = int(sizes[1].replace('楼', '').strip())
    dic['structure'] = sizes[2].strip()
    dic['direction'] = sizes[3].strip()


def parse_location(location_str, dic):
    locations = location_str.split('  ')
    dic['community'] = locations[1]


def parse_id(url):
    m = id_pat.match(url)
    return m.group(1) if m else 0


def get_next(response):
    classes = response.selector.xpath('//div[@class="page"]/a')
    if len(classes) < 2:
        return False

    next_url = classes[-1].xpath('./@href')[0].extract().strip()
    return next_url


def main():
    print('do sth')


if __name__ == '__main__':
    main()
