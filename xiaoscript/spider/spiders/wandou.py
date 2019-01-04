#!/usr/bin/env python
# encoding: utf-8

"""
@description: 豌豆荚爬虫

@author: baoqiang
@time: 2019/1/4 下午12:56
"""
import scrapy
from scrapy.http import FormRequest
import json
from xiaoscript.config import get_root_path
import time
from scrapy.selector import Selector
import re
import threading

url_fmt = 'https://www.wandoujia.com/wdjweb/api/top/more?resourceType=0&page={}&ctoken=8zZ7f4MGTQAYySTy6p4X2_4v'
out_file = '{}/wandou.json'.format(get_root_path())
root_url = 'https://www.wandoujia.com'


class WandouSpider(scrapy.Spider):
    name = 'wandou'
    num = 1
    lock = threading.Lock()

    def start_requests(self):
        for i in range(1, 134000):
        # for i in range(0, 3):
            url = url_fmt.format(i)
            yield FormRequest(url, callback=self.parse_cate)

    def parse_cate(self, response):

        datas = []

        jdata = json.loads(response.body_as_unicode())
        root = Selector(text=jdata['data']['content'])

        classes = root.xpath('.//li')
        for item in classes:
            # dic = {"from_url": response.request.url}
            dic = {}

            # add id
            self.lock.acquire()
            dic["id"] = self.num
            self.num += 1
            self.lock.release()

            # title
            title_url = item.xpath('.//h2[@class="app-title-h2"]/a')
            dic['title'] = title_url.xpath('./@title')[0].extract().strip()
            dic['url'] = title_url.xpath('./@href')[0].extract().strip()

            # meta
            meta_url = item.xpath('.//div[@class="meta"]')
            install_str = meta_url.xpath('./span[@class="install-count"]/text()')[0].extract().strip()
            dic['cnt'] = int(trim_install(install_str))

            # comment
            comment_url = item.xpath('.//div[@class="comment"]')
            dic['comment'] = comment_url.xpath('./text()')[0].extract().strip()

            # tag
            tag_url = item.xpath('./a[@class="tag-link"]')
            dic['tag'] = tag_url.xpath('./text()')[0].extract().strip()
            tag_url_str = tag_url.xpath('./@href')[0].extract().strip()
            dic['tag_url'] = trim_tag_url(tag_url_str)

            datas.append(dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for dic in datas:
                json.dump(dic, fw, ensure_ascii=False)
                fw.write('\n')


def trim_install(src):
    src = src.replace('人下载', '')
    if not src:
        src = '0'

    if '万' in src:
        src = src.replace('万', '')
        return float(src) * 1e4

    if '亿' in src:
        src = src.replace('亿', '')
        return float(src) * 1e8

    return float(src)


regex = re.compile('\?.*$')


def trim_tag_url(src):
    m = regex.search(src)
    if m:
        replaced = m.group()
        return src.replace(replaced, "")
    return src


if __name__ == '__main__':
    print(int(time.time() * 1000))
