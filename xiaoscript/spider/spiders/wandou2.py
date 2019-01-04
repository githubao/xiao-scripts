#!/usr/bin/env python
# encoding: utf-8

"""
@description: 豌豆荚爬虫，根据类别

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

start_cate_url = 'https://www.wandoujia.com/category/app'
item_cate_fmt = 'https://www.wandoujia.com/wdjweb/api/category/more?catId={}&subCatId={}&page={}&ctoken=ZnrB6v38kAfy6a1GyghJGGtM'
out_file = '{}/wandou2.json'.format(get_root_path())

root_url = 'https://www.wandoujia.com'
cate_url = 'https://www.wandoujia.com/category/'


class Wandou2Spider(scrapy.Spider):
    name = 'wandou2'
    num = 1
    lock = threading.Lock()

    def start_requests(self):
        yield FormRequest(start_cate_url, callback=self.parse_cate)

    def parse_cate(self, response):
        data = []

        classes = response.selector.xpath('.//li[@class="parent-cate"]')
        for item in classes:
            title = item.xpath('./a/text()')[0].extract().strip()
            subclasses = item.xpath('./div[@class="child-cate"]')
            for subitem in subclasses:
                subtitle = subitem.xpath('./a/@title')[0].extract().strip()
                suburl = subitem.xpath('./a/@href')[0].extract().strip()

                cate, subcate = parse_cate(suburl)
                data.append({'cate1': title, 'cate2': subtitle, 'cate1_id': cate, 'cate2_id': subcate})

        for item in data:
            url = item_cate_fmt.format(item['cate1_id'], item['cate2_id'], 1)
            yield FormRequest(url, callback=self.parse_item, meta=item)
            # break

    def parse_item(self, response):
        meta = response.meta

        datas = []

        jdata = json.loads(response.body_as_unicode())
        root = Selector(text=jdata['data']['content'])

        classes = root.xpath('.//li')
        for item in classes:
            dic = {"from_url": response.request.url, 'cate1': meta['cate1'], 'cate2': meta['cate2'],
                   'cate1_id': meta['cate1_id'], 'cate2_id': meta['cate2_id']}

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
            dic['cate_url'] = '{}{}_{}'.format(cate_url, meta['cate1_id'], meta['cate2_id'])

            datas.append(dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for dic in datas:
                json.dump(dic, fw, ensure_ascii=False)
                fw.write('\n')

        # yield next
        cur_page = jdata['data']['currPage']
        # if cur_page != -1:
        if cur_page != -1 and cur_page < 100:
            url = item_cate_fmt.format(meta['cate1_id'], meta['cate2_id'], cur_page + 1)
            yield FormRequest(url, callback=self.parse_item, meta=meta)


def trim_install(src):
    src = src.replace('人下载', '').replace('人安装', '')
    if not src:
        src = '0'

    if '万' in src:
        src = src.replace('万', '')
        return float(src) * 1e4

    if '亿' in src:
        src = src.replace('亿', '')
        return float(src) * 1e8

    return float(src)


cate_re = re.compile('^https://www.wandoujia.com/category/(\d+)_(\d+)$')


def parse_cate(cate_url):
    m = cate_re.search(cate_url)
    if m:
        return m.group(1), m.group(2)
    return 0, 0


if __name__ == '__main__':
    print(int(time.time() * 1000))
