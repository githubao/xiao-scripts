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
import pandas as pd

ZIROOM = 'ziroom'

keywords = ['来广营', '东湖渠', '望京']

root_path = '/Users/baoqiang/Downloads/'
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


def to_excel():
    """
    自如接口爬虫来的数据
    :return:
    """
    house_url_fmt = 'http://www.ziroom.com/z/vr/{}.html'

    input_file = root_path + 'ziru3.json'
    out_file = root_path + 'ziru3.xlsx'

    df = read_json(input_file)

    # 添加url
    df['url'] = df['id'].map(lambda x: house_url_fmt.format(x))

    # 指定列的顺序
    cols = ['id', 'subway_line_code_first', 'subway_station_code_first', 'sell_price',
            'usage_area', 'house_facing', 'title', 'room_name', 'url', 'resblock_name',
            'build_size', 'dispose_bedroom_amount', 'walking_distance_dt_first']
    df = df.loc[:, cols]

    # 去重id重复的记录
    df = df.drop_duplicates('id')

    # 添加超链接
    df['url'] = df['url'].map(lambda x: make_hyperlink(x))

    # 去除"约"
    df['usage_area'] = df['usage_area'].map(lambda x: float('{}'.format(x).replace('约', '')))
    df['build_size'] = df['build_size'].map(lambda x: float('{}'.format(x).replace('约', '')))

    df.to_excel(out_file, index=False)


def read_json(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        datas = (line.strip() for line in f)
        datas = '[{}]'.format(','.join(datas))

    return pd.read_json(datas)


def make_hyperlink(value):
    # url = "https://custom.url/{}"
    return '=HYPERLINK("%s", "%s")' % (value, value)


if __name__ == '__main__':
    run()
    to_excel()
