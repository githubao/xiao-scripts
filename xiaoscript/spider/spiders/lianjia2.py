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

# out_file = 'C:\\Users\\xiaobao\\Desktop\\lianjia.json'
# out_file = '/mnt/home/baoqiang/lianjia.json'
out_file = '/Users/baoqiang/Downloads/lianjia.json'

curl = 'https://bj.lianjia.com/ershoufang/chaoyang/l2l3ba70ea130bp400ep550/'
conditions = 'l2l3ba70ea130bp400ep550'


class Lianjia2Spider(scrapy.Spider):
    name = 'lianjia2'

    def start_requests(self):
        return [Request('https://bj.lianjia.com/ershoufang/', callback=self.parse_area)]

    def parse_area(self, response):
        classes = response.selector.xpath('//div[@class="position"]//div[@data-role="ershoufang"]//a')
        for item in classes:
            url = '{}{}'.format(root_url, item.xpath('./@href')[0].extract())

            if 'lf.lianjia' in url:
                continue

            # if 'chaoyang' not in url:
            #     continue

            if 'haidian' not in url:
                continue

            yield Request(url, callback=self.parse_page)

            # break

    def parse_page(self, response):
        pg_num = get_pg_num(response)

        for i in range(1, pg_num + 1):
            # yield Request('{}pg{}/'.format(response.url, i), callback=self.parse_list)
            yield Request('{}pg{}{}/'.format(response.url, i, conditions), callback=self.parse_list)

            # break

    def parse_list(self, response):
        classes = response.selector.xpath(
            '//ul[@class="sellListContent"]//li[contains(@class,"clear")]//div[@class="title"]/a/@href')

        for item in classes:
            url = item.extract().strip()
            yield Request(url, callback=self.parse_item)

            # break

    def parse_item(self, response):
        dic = {'url': response.url}

        body = response.selector.xpath('//body')

        # 标题和文本
        dic['title'] = body.xpath('.//h1/text()')[0].extract().strip()
        idurl = body.xpath('.//div[@class="houseRecord"]/span[@class="info"]/text()')
        dic['id'] = int(idurl[0].extract().strip('\'"').strip())

        # 价格信息
        dic['price'] = float(
            body.xpath('.//div[contains(@class,"price")]/span[@class="total"]/text()')[0].extract().strip())
        dic['unit'] = float(body.xpath('.//span[@class="unitPriceValue"]/text()')[0].extract().strip())

        # 关注人数
        dic['fav_count'] = int(body.xpath('.//span[@id="favCount"]/text()')[0].extract().strip())

        # 基本信息
        houseurl = body.xpath('.//div[@class="houseInfo"]')
        dic['structure'] = houseurl.xpath('./div[@class="room"]//text()')[0].extract().strip()
        dic['direction'] = houseurl.xpath('./div[@class="type"]//text()')[0].extract().strip()
        dic['size'] = float(houseurl.xpath('./div[@class="area"]//text()')[0].extract().strip().replace('平米', ''))

        # 社区信息
        communityurl = body.xpath('.//div[@class="communityName"]/a[contains(@class,"info")]')
        dic['community'] = communityurl.xpath('./text()')[0].extract().strip()

        # 位置信息
        areaurl = body.xpath('.//div[@class="areaName"]/span[contains(@class,"info")]//text()')
        dic['district'] = areaurl[0].extract().strip()
        dic['town'] = areaurl[2].extract().strip()
        dic['street'] = areaurl[3].extract().strip() if len(areaurl) > 2 else '_'

        # 地铁信息
        subwayurl = body.xpath('.//div[@class="areaName"]/a[@class="supplement"]/text()')
        dic['subway'] = subwayurl[0].extract().strip() if subwayurl else '_'

        # 其他信息
        introurl = body.xpath('.//div[@class="introContent"]')
        update_dic(introurl, dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            json.dump(dic, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')


def update_dic(infourl, dic):
    baseurl = infourl.xpath('./div[@class="base"]//ul/li')

    for item in baseurl:
        name = item.xpath('./span/text()')[0].extract().strip()
        value = item.xpath('./text()')[0].extract().strip()

        if name == '套内面积':
            try:
                dic['size_inuse'] = float(value.replace('㎡', '').strip())
            except Exception as e:
                dic['size_inuse'] = 0

        if name == '所在楼层':
            dic['floor'] = value

    transactionurl = infourl.xpath('./div[@class="transaction"]//ul/li')
    for item in transactionurl:
        name = item.xpath('./span/text()')[0].extract().strip()
        value = item.xpath('./span/text()')[1].extract().strip()

        if name == '交易权属':
            dic['transact_type'] = value

        if name == '房屋用途':
            dic['house_type'] = value


def get_pg_num(response):
    div = response.selector.xpath('//div[contains(@class,"house-lst-page-box")]')
    page_data = div.xpath('./@page-data')[0].extract()
    return json.loads(page_data)['totalPage']


root_url = 'https://bj.lianjia.com'


def main():
    print('do sth')


if __name__ == '__main__':
    main()
