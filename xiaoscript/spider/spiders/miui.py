#!/usr/bin/env python
# encoding: utf-8

"""
@description: 小米的主题爬虫

@author: baoqiang
@time: 2018/12/6 下午8:26
"""

import scrapy
from scrapy.http import FormRequest
import json
from xiaoscript.config import get_root_path
import time

url_fmt = 'http://zhuti.xiaomi.com/compound?page={}&sort=New'
comment_fmt = 'http://zhuti.xiaomi.com/comment/listall/{}?page=0&t={}&status=3'
out_file = '{}/miui.json'.format(get_root_path())
root_url = 'http://zhuti.xiaomi.com'


class MiuiSpider(scrapy.Spider):
    name = 'miui'

    def start_requests(self):
        for i in range(1, 1225):
        # for i in range(1, 3):
            url = url_fmt.format(i)
            yield FormRequest(url, callback=self.parse_cate)

    def parse_cate(self, response):
        datas = []

        classes = response.selector.xpath('.//div[contains(@class,"page_list")]//ul[@class="thumb-list"]/li')
        for item in classes:
            dic = {"from_url": response.request.url}

            title_url = item.xpath('./div[@class="title"]/a')
            dic['title'] = title_url.xpath('./@title')[0].extract().strip()
            href = title_url.xpath('./@href')[0].extract().strip()
            dic['url'] = root_url + href
            dic['id'] = href.replace('/detail/', '').replace("-", '')

            rank_url = item.xpath('./div[@id="commentRankPoint"]')
            dic['price'] = rank_url.xpath('./span/text()')[0].extract().strip().replace('米币', '')
            dic['rank'] = int(rank_url.xpath('@class')[0].extract().strip().replace('rank_list rl', ''))

            datas.append(dic)

        for dic in datas:
            comment_url = comment_fmt.format(dic['url'].replace(root_url + '/detail/', ''), int(time.time() * 1000))
            yield FormRequest(comment_url, callback=self.parse_item2, meta={'dic': dic})

    def parse_item(self, response):
        dic = response.meta['dic']

        page_url = response.selector.xpath('.//div[@id="commTurnPage"]/span/text()')

        if page_url:
            dic['comment'] = page_url[-1].extract().strip().replace('共', '').replace('页', '')
        else:
            dic['comment'] = 0

        with open(out_file, 'a', encoding='utf-8') as fw:
            json.dump(dic, fw, ensure_ascii=False)
            fw.write('\n')

    def parse_item2(self, response):
        """
        处理json数据
        :param response:
        :return:
        """
        dic = response.meta['dic']

        jdata = json.loads(response.body_as_unicode())
        dic['comment'] = jdata['commentCount']

        with open(out_file, 'a', encoding='utf-8') as fw:
            json.dump(dic, fw, ensure_ascii=False)
            fw.write('\n')


if __name__ == '__main__':
    print(int(time.time() * 1000))
