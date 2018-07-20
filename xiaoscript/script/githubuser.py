#!/usr/bin/env python
# encoding: utf-8

"""
@description: 爬取github的用户

@author: baoqiang
@time: 2018/7/20 上午10:40
"""

import json
import os
from collections import OrderedDict

import requests

cur_dir = os.path.split(os.path.realpath(__file__))[0]

out_file = cur_dir + '/../data/github_tmp.json'
out_file2 = cur_dir + '/../data/github.json'


def req_api():
    # auth = input('email: '), input('password: ')
    auth = 'mailbaoqiang@gmail.com', input('password: ')

    url_fmt = 'https://api.github.com/orgs/apache/repos?page={}&per_page=100'

    for i in range(1, 21):
        # for i in range(1, 3):
        url = url_fmt.format(i)

        resp = requests.get(url, auth=auth)

        datas = _process_resp(resp.json())

        with open(out_file, 'a') as fw:
            for item in datas:
                json.dump(item, fw)
                fw.write('\n')

        print('process num: {}'.format(i))


def sort_items():
    res = []

    with open(out_file, 'r') as f:
        for line in f:
            jdata = json.loads(line.strip(), object_pairs_hook=OrderedDict)
            res.append(jdata)

    res.sort(key=lambda x: x['stars'] + x['forks'], reverse=True)

    with open(out_file2, 'w') as fw:
        for item in res:
            json.dump(item, fw)
            fw.write('\n')


def _process_resp(jdata):
    res = []

    for item in jdata:
        dic = OrderedDict()

        _hack(item)

        for field in need_fields:
            dic[field] = item[field]

        res.append(dic)

    return res


def _hack(dic):
    dic['url'] = dic['html_url']
    dic['stars'] = dic['stargazers_count']


need_fields = ['id', 'url', 'name', 'description', 'language',
               'forks', 'stars', 'created_at', 'updated_at', 'full_name']


def run():
    req_api()
    sort_items()


if __name__ == '__main__':
    run()
