#!/usr/bin/env python
# encoding: utf-8

"""
@description: 自如 区域 爬虫

@author: pacman
@time: 2018/3/2 15:56
"""

import scrapy
from scrapy import Request
import json
import re
import urllib.parse
import traceback
from xiaoscript import config

start_url = 'http://www.ziroom.com/z/nl/z3.html'

out_file = '{}/ziru2.json'.format(config.get_root_path())

id_pat = re.compile('http://www.ziroom.com/z/vr/([\d]+).html')


# url = 'http://www.ziroom.com/z/nl/-z3-s1号线-t苹果园.html'

class Ziru2Spider(scrapy.Spider):
    name = 'ziru2'

    def start_requests(self):
        yield Request(start_url, callback=self.parse_line)

    def parse_line(self, response):
        classes = response.selector.xpath('.//dl[contains(@class,"zIndex6")]//li')
        for item in classes:
            line_url = item.xpath('./span[@class="tag"]/a')

            if not line_url:
                continue

            district = line_url.xpath('./text()')[0].extract().strip()

            sub_classes = item.xpath('./div[@class="con"]//a')
            for subitem in sub_classes:
                url = subitem.xpath('./@href')[0].extract().strip()
                url = 'http:{}'.format(url)
                town = subitem.xpath('./text()')[0].extract().strip()

                if '全部' == town:
                    continue

                if '朝阳' != district:
                    continue

                yield Request(url, meta={'district': district, 'town': town, 'start': True}, callback=self.parse_page)

                # return

    def parse_page(self, response):
        district = response.meta['district']
        town = response.meta['town']

        classes = response.selector.xpath('.//ul[@id="houseList"]/li')

        results = []
        for item in classes:
            dic = {'district': district, 'town': town, 'from_url': urllib.parse.unquote(response.url)}

            url = item.xpath('.//div[@class="txt"]/h3/a/@href')
            dic['url'] = 'http:{}'.format(url[0].extract().strip())
            dic['id'] = parse_id(dic['url'])

            dic['title'] = item.xpath('.//div[@class="txt"]/h3//text()')[0].extract().strip()
            dic['sub_title'] = item.xpath('.//div[@class="txt"]/h4//text()')[0].extract().strip()

            price_url = item.xpath('.//p[@class="price"]//text()')[0].extract().strip()
            # dic['price'] = float(price_url.replace('￥', '').strip())
            dic['price'] = ""

            # 更新细节信息
            details_url = item.xpath('.//div[@class="txt"]/div[@class="detail"]')
            update_dic(details_url, dic)

            results.append(dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

        if response.meta['start']:
            num = get_pg_num(response)

            if num < 2:
                return

            for i in range(2, num + 1):
                req_url = '{}?p={}'.format(response.url, i)
                yield Request(req_url, meta={'district': district, 'town': town, 'start': False},
                              callback=self.parse_page)

                # break


def update_dic(url, dic):
    p0_url = url.xpath('./p')[0]

    txts_url = p0_url.xpath('.//text()')
    txts = [item.extract().strip() for item in txts_url if item.extract().strip() != '|']
    txts = [item for item in txts if item]

    try:
        if len(txts) > 0:
            dic['size'] = float(txts[0].replace('㎡', '').replace('约', '').strip())
        if len(txts) > 1:
            dic['floor'] = txts[1]
        if len(txts) > 2:
            dic['structure'] = txts[2]

    except Exception as e:
        traceback.print_exc()

    p1_url = url.xpath('./p')
    if len(p1_url) > 1:
        subway_url = p1_url[1].xpath('.//text()')
        dic['distance'] = subway_url[0].extract().strip() if subway_url else 0


def parse_id(url):
    m = id_pat.match(url)
    return m.group(1) if m else 0


def get_pg_num(response):
    classes = response.selector.xpath('//div[@class="pages"]/a')
    if len(classes) < 2:
        return 1

    item = classes[-2]

    pg_num = item.xpath('./text()')[0].extract().strip()
    return int(pg_num)


def main():
    print('do sth')


if __name__ == '__main__':
    main()
