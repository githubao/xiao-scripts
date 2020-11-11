#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: baoqiang
@time: 2020/11/11 1:19 下午
"""

import json
import pandas as pd

root_path = '/users/baoqiang/downloads'


def process():
    input_file = root_path + '/lianjia.json'
    out_file = root_path + '/lianjia.xlsx'

    df = read_json(input_file)

    # id修改
    df['id'] = df['id'].apply(lambda x: 'A{}'.format(x))

    # 过滤
    df = df[(df['price'] >= 400) & (df['price'] <= 600) & (df['size'] >= 60)]

    # 过滤
    df = df[(~df['structure'].str.contains('房间')) & (~df['floor'].str.contains('地下室'))
            & (~df['structure'].str.contains('1室'))]

    # 添加超链接
    df['url'] = df['url'].apply(lambda x: make_hyperlink(x))

    # 指定列的顺序
    cols = ['id', 'title', 'price', 'size', 'fav_count',
            'district', 'town', 'street', 'subway', 'community',
            'floor', 'structure', 'direction',
            'url', 'size_inuse', 'unit']
    df = df.loc[:, cols]

    # 按照多个字段排序
    df = df.sort_values(by=['fav_count'], ascending=[False])

    df.to_excel(out_file, index=False)


def read_json(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        datas = (line.strip() for line in f)
        datas = '[{}]'.format(','.join(datas))

    return pd.read_json(datas)


def make_hyperlink(value):
    return '=HYPERLINK("%s", "%s")' % (value, value)


def custom_sort(dic):
    keys = ['id', 'title', 'price', 'size', 'fav_count',
            'district', 'town', 'street', 'subway', 'community',
            'floor', 'structure', 'direction',
            'url', 'size_inuse', 'unit']
    sorted_lst = []

    for key in keys:
        sorted_lst.append((key, dic.get(key, 0)))

    return sorted_lst


if __name__ == '__main__':
    process()

"""
必须条件: 
60平以上，400-600万，至少是两室
位置是最重要的，位置和大小优选位置
尽量条件: 板楼(南北通透,向阳)，有电梯

备选：


"""


