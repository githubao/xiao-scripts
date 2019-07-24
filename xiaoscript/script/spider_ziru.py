#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: baoqiang
@time: 2018/11/28 下午10:05
"""

import requests
import json

from xiaoscript import config

ZIROOM = 'ziroom'

# keywords = ['望京', '望京西', '阜通']
keywords = ['六道口', '清华东路西口','五道口']

out_file = '{}/ziru3.json'.format(config.get_root_path())


def run():
    for keyword in keywords:
        print('process {}'.format(keyword))
        run_item(keyword)


def run_item(keyword):
    datas = []

    for i in range(10, 10001, 10):
        # for i in range(10, 30, 10):
        payload = {'step': i, 'key_word': keyword}
        res = requests.post('http://m.ziroom.com/list/ajax-get-data', data=payload, headers=headers)
        if 'info' in res.json()['data'] and res.json()['data']['info'] == u'\u6570\u636e\u52a0\u8f7d\u5b8c\u6bd5':
            break
        for item in res.json()['data']:
            datas.append(item)

        print('process cnt: {}/{}'.format(i, 10000))

    with open(out_file, 'a', encoding='utf-8') as fw:
        for item in datas:
            json.dump(item, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')


headers = {'Referer': 'http://m.ziroom.com/BJ/search.html',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/57.0.2987.133 Safari/537.36'}

if __name__ == '__main__':
    run()
