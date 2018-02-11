#!/usr/bin/env python
# encoding: utf-8

"""
@description: api的接口有权限认证，所以尝试使用网页爬虫

@author: pacman
@time: 2018/2/11 13:07
"""

import scrapy
from scrapy import Request
import json
import traceback

out_file = 'C:\\Users\\xiaobao\\Desktop\\lianjia.txt'


class Lianjia2Spider(scrapy.Spider):
    name = 'lianjia2'

    def start_requests(self):
        return [Request('https://bj.lianjia.com/ershoufang/', callback=self.parse_area)]

    def parse_area(self, response):
        classes = response.selector.xpath('//div[@class="position"]//div[@data-role="ershoufang"]//a')
        for item in classes:
            url = '{}{}'.format(root_url, item.xpath('./@href')[0].extract())

            if 'lf.lianjian' in url:
                continue

            yield Request(url, callback=self.parse_page)

            break

    def parse_page(self, response):
        pg_num = get_pg_num(response)

        for i in range(1, pg_num + 1):
            yield Request('{}pg{}/'.format(response.url, i), callback=self.parse_list)

            break

    def parse_list(self, response):
        classes = response.selector.xpath('//ul[@class="sellListContent"]//li[@class="clear"]//div[@class="title"]/a')

        results = []
        for item in classes:
            dic = {'from_url': response.url}

            aurl = item.xpath('.//')
            dic['url'] = aurl.xpath('./@href')[0].extract().strip()
            dic['id'] = int(aurl.xpath('./@data-housecode')[0].extract().strip())
            dic['title'] = aurl.xpath('./text()')[0].extract().strip().replace('\t', '')

            try:
                infourl = item.xpath('.//div[@class="houseInfo"]')
                update_dic(infourl, dic)

                totalurl = item.xpath('.//div[@class="totalPrice"]')
                dic['total_price'] = ''.join(i.extract().strip() for i in totalurl.xpath('.//text()'))

                uniturl = item.xpath('.//div[@class="unitPrice"]')
                dic['unit_price'] = int(uniturl.xpath('./@data-price')[0].extract().strip())

            except Exception as e:
                traceback.print_exc()

            results.append(dic)

            break

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')


def update_dic(infourl, dic):
    aurl = infourl.xpath('./a')
    if aurl:
        dic['xiaoqu'] = aurl.xpath('./text()')[0].extract().strip()

    spans = infourl.xpath('.//span//text()')

    for item in spans:
        text = item.extract().strip()
        if '室' in text or '厅' in text:
            dic['huxing'] = text
        if '平米' in text:
            dic['size'] = int(text.replace('平米', ''))
        if '东' in text or '西' in text or '南' in text or '北' in text:
            dic['direction'] = text


def get_pg_num(response):
    div = response.selector.xpath('//div[contains(@class,"house-lst-page-box")]')
    page_data = div.xpath('./@page-data')[0].extract()
    return json.loads(page_data)['totalPage']


root_url = 'https://bj.lianjia.com'


def main():
    print('do sth')


if __name__ == '__main__':
    main()
