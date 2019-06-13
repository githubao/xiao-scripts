#!/usr/bin/env python
# encoding: utf-8

"""
@description: 2019北京二手房源分析

@author: baoqiang
@time: 2019-06-13 12:47
"""

import json
import pandas as pd

root_path = '/users/baoqiang/downloads'


def process():
    with open('{}/lianjia.json'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/lianjia.csv'.format(root_path), 'w', encoding='utf-8') as fw:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            json_data = json.loads(line.strip())

            # filter
            price = json_data['price']
            if price > 400:
                continue

            size = float(json_data['size'])
            if size < 50:
                continue

            structure = json_data['structure']
            if '1室' in structure:
                continue

            # 粘贴到excel id显示异常的问题
            json_data['id'] = 'A{}'.format(json_data['id'])

            sorted_list = custom_sort(json_data)

            if idx == 1:
                for k, v in sorted_list:
                    fw.write('{},'.format(k))
                fw.write('\n')

            for k, v in sorted_list:
                fw.write('{},'.format(v))
            fw.write('\n')


def process_pd():
    input_file = root_path + '/lianjia.json'
    out_file = root_path + '/lianjia.xlsx'

    df = read_json(input_file)

    # id修改
    df['id'] = df['id'].apply(lambda x: 'A{}'.format(x))

    # 过滤
    df = df[(df['price'] <= 400) & (df['size'] >= 50) & (~df['structure'].str.contains('1室'))]

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
    # process()
    process_pd()

"""
必须条件: 
50平以上，小于500万，至少是两室

尽量条件：
1. 位置是最重要的，位置和大小优选位置
2. 尽量400万以内，500万是上限

加分条件：
1. 板楼，向阳，南北通透

notice:
1. 优先等额本息贷款

解释：
1. 等额本息还款金额一直一样，前期还款压力小，未来的钱越来越不值钱

"""

"""
数据

"""

"""
备选
"""
