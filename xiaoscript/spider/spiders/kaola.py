#!/usr/bin/env python
# encoding: utf-8

"""
@description: kaola爬虫

@author: baoqiang
@time: 2019-05-15 20:45
"""

import json

import scrapy
from scrapy import FormRequest
import sys
import re
import requests
import logging

from xconcurrent import threadpool
from xiaoscript.config import get_root_path

out_file = '{}/kaola.json'.format(get_root_path())
task_file = '{}/kaola_task.json'.format(get_root_path())
start_url = 'https://www.kaola.com'


class KaolaSpider(scrapy.Spider):
    name = 'kaola'
    cnt = 0
    processed_set = set()

    def start_requests(self):
        yield FormRequest(start_url, callback=self.parse_cate)

    def parse_cate(self, response):
        datas = []

        classes = response.selector.xpath('.//div[@class="litd"]//a[@class="cat2"]')

        for item in classes:
            dic = {}

            cate = item.xpath('./@href')[0].extract().strip()
            dic['cate'] = cate

            name = item.xpath('./text()')[0].extract().strip()
            dic['name'] = name

            datas.append(dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in datas:
                json.dump(item, fw, ensure_ascii=False)
                fw.write('\n')


def run_requests():
    url = 'https://search.kaola.com/api/getFrontCategory.shtml'
    resp = requests.get(url)

    jdata = resp.json()

    for item in jdata['body']['frontCategoryList']:
        cid = item['categoryId']
        cname = item['categoryName']

        for subitem in item['childrenNodeList']:
            subcid = subitem['categoryId']
            subcname = subitem['categoryName']

            # print('{}-{} {}-{}'.format(cid, cname, subcid, subcname))
            yield cid, cname, subcid, subcname


def run_requests2(subcid):
    # pat = re.compile('data-id="([\\d]+)" title="(.*?)"')
    pat = re.compile('brandList=([^;]{10,});')

    req_url = 'https://search.kaola.com/category/{}.html'.format(subcid)

    resp = requests.get(req_url)

    m = pat.search(resp.content.decode())

    if not m:
        sys.exit(1)

    jdata = json.loads(m.group(1))

    logging.info('brand size: {} {}'.format(subcid, len(jdata)))

    for item in jdata:
        bid = item['brandId']
        bname = item['brandName']

        # print('{}-{}'.format(bid, bname))
        yield bid, bname


def run_requests3(bid):
    pat = re.compile('([\\d]+)</span>人关注该品牌')
    # pat = re.compile('([\\d]+)人关注该品牌')

    url = 'https://search.kaola.com/brand/{}.html'.format(bid)
    resp = requests.get(url)
    m = pat.search(resp.content.decode())

    # text = 'ocusCount">996887</span>人关注该品牌'
    # m = pat.search(text)

    if not m:
        sys.exit(1)

    return int(m.group(1))


def schedule():
    with open(out_file, 'w', encoding='utf-8') as fw:
        for a, b, c, d in run_requests():
            for x, y in run_requests2(c):
                dic = {
                    'cid': a,
                    'cname': b,
                    'subcid': c,
                    'subname': d,
                    'bid': x,
                    'bname': y,
                    'favor_cnt': run_requests3(x),
                }
                json.dump(dic, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')
                fw.flush()

                # sys.exit(2)

            logging.info('process cate: {}'.format(a))


class MultiKaola(threadpool.MultiRun):
    def run_one(self, dic):
        dic['favor_cnt'] = run_requests3(dic['bid'])
        return dic


def build_task():
    tasks = []

    for a, b, c, d in run_requests():
        for x, y in run_requests2(c):
            dic = {
                'cid': a,
                'cname': b,
                'subcid': c,
                'subname': d,
                'bid': x,
                'bname': y,
            }

            tasks.append(dic)

    # write to file
    with open(task_file, 'w', encoding='utf-8') as fw:
        for dic in tasks:
            json.dump(dic, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')

    return tasks


def build_task_from_file():
    tasks = []

    with open(task_file, 'r', encoding='utf-8') as fw:
        for line in fw:
            dic = json.loads(line.strip())

            if dic['bid'] not in [3017, 1452]:
                continue

            tasks.append(dic)

    return tasks


def multi_kaola():
    tasks = build_task_from_file()

    logging.info('task len: {}'.format(len(tasks)))
    if len(tasks) != 2:
        sys.exit(3)

    multi = MultiKaola(tasks)

    with open(out_file, 'a', encoding='utf-8') as fw:
        for item in multi.run_many():
            if item is None:
                continue

            json.dump(item, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')


def get_none():
    for one in one_none():
        print(one)


def one_none():
    for i in range(3):
        if i == 1:
            yield None
        else:
            yield i


if __name__ == '__main__':
    # schedule()
    multi_kaola()
    # get_none()
