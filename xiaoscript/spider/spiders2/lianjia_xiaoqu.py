#!/usr/bin/env python
# encoding: utf-8

"""
@description: 链家小区

@author: baoqiang
@time: 2019-07-24 12:49
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from xiaoscript import config
from threading import Lock
import json
import re
from scrapy import Request

start_url = 'https://bj.lianjia.com/xiaoqu/'

id_pat = re.compile('https://bj.lianjia.com/xiaoqu/([\\d]+)')

out_file = '{}/lianjia_xiaoqu.json'.format(config.get_root_path())


class LjXiaoquSpider(CrawlSpider):
    name = 'lj_xiaoqu_spider'
    start_urls = [start_url, ]

    links1 = LinkExtractor(allow='.*/xiaoqu/[a-z]+/(pg[\\d]+){0,1}$')

    rules = (
        Rule(links1, callback='parse_cate', follow=True),
    )

    lock = Lock()
    ids = set()

    def parse_cate(self, response):
        classes = response.selector.xpath(
            './/div[@class="leftContent"]//ul[@class="listContent"]/li')

        datas = []

        for item in classes:
            dic = {'from_url': response.url}

            title_url = item.xpath('.//div[@class="title"]/a')
            dic['url'] = title_url.xpath('./@href')[0].extract().strip()
            dic['xiaoqu'] = title_url.xpath('./text()')[0].extract().strip()

            chengjiao_url = item.xpath('.//div[@class="houseInfo"]//a/text()')
            dic['chengjiao'] = get_chengjiao(chengjiao_url)

            district_url = item.xpath('.//a[@class="district"]//text()')
            dic['district'] = district_url[0].extract().strip()

            bizcircle_url = item.xpath('.//a[@class="bizcircle"]//text()')
            dic['bizcircle'] = bizcircle_url[0].extract().strip()

            info_url = item.xpath('.//div[@class="positionInfo"]/text()')
            info = ''.join(i.extract().strip() for i in info_url)
            dic['struct'], dic['year'] = parse_info(info)
            dic['year'] = parse_year(dic['year'])

            price_url = item.xpath('.//div[@class="totalPrice"]/span/text()')
            dic['price'] = safe_price(price_url[0].extract().strip())

            sell_url = item.xpath('.//a[@class="totalSellCount"]/span/text()')
            dic['sell_count'] = int(sell_url[0].extract().strip())

            dic['id'] = parse_id(dic['url'])

            # add one
            if not dic['id'] in self.ids:
                datas.append(dic)
                self.ids.add(dic['id'])

        self.write_file(datas)

        # next pages
        if 'pg' not in response.url:
            m = re.search('"totalPage":(\\d+)', response.text)

            if not m:
                return

            total_page = int(m.group(1))

            for i in range(2, total_page + 1):
                url = '{}pg{}/'.format(response.url, i)
                yield Request(url, callback=self.parse_cate)

    def write_file(self, results):
        self.lock.acquire()

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

        self.lock.release()


def safe_price(price_str):
    try:
        return int(price_str)
    except ValueError as e:
        return 0


def parse_id(url):
    m = id_pat.match(url)
    if m:
        return m.group(1)
    else:
        return 0


def parse_info(info):
    items = info.split('\n')
    a, b = '', ''

    if len(items) == 2:
        a = items[0].replace('/', '').replace(' ', '')
        b = items[1].replace('/', '').replace(' ', '')

    return a, b


def get_chengjiao(chengjiao_url):
    for item in chengjiao_url:
        txt = item.extract().strip()

        if '30天成交' in txt:
            return int(txt.replace('30天成交', '').replace('套', ''))

    return 0


def parse_year(year_str):
    if '未知' in year_str:
        return 0
    return int(year_str.strip().replace('年建成', ''))


if __name__ == '__main__':
    info = '/塔板结合\n / 1979年建成'
    print(parse_info(info))
