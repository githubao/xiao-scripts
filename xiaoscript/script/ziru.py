#!/usr/bin/env python
# encoding: utf-8

"""
@description: 处理自如的爬虫数据，分析得到最应该租住的区域

@author: pacman
@time: 2018/3/2 17:29
"""

import json
from xiaoscript import config
import re

root_path = config.get_root_path()

floor_pat = re.compile('([\d]+)/([\d]+)层')
distance_pat = re.compile('([\d]+)米')

processed_ids = set()


def process():
    not_print_key = True

    with open('{}/ziru.json'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/ziru.txt'.format(root_path), 'w', encoding='utf-8') as fw:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            json_data = json.loads(line.strip())

            # 重复
            uid = json_data['id']
            if uid in processed_ids:
                continue
            else:
                processed_ids.add(uid)

            # 价格
            price = float(json_data['price'])
            if price < 500:
                json_data['price'] = price * 30
            else:
                json_data['price'] = price

            # if json_data['price'] > 3500:
            #     continue

            # 整租 或者 合租两居室
            # structure = json_data['structure']
            # if not ('1室' in structure or '2室' in structure):
            #     continue

            # line = json_data['line']
            # if line not in ['13号线', '昌平线', '8号线', '5号线']:
            #     continue

            # 房间大小
            size = json_data['size']
            if size < 10:
                continue

            # 房间朝向
            title = json_data['title']
            if '南' not in title:
                continue

            # 地理位置
            sub_title = json_data['sub_title']
            if not lst_contains(sub_title, ['朝阳', '海淀', '昌平']):
                continue

            # 处理楼层
            floor = json_data['floor']
            json_data['in_floor'], json_data['floor'] = split_floor(floor)

            # 处理地铁线距离
            json_data['subway_distance'] = trim_distance(json_data['subway_distance'])

            # 按照想要的key的顺序排序
            sorted_dic = custom_sort(json_data)

            if not_print_key:
                key = '\t'.join(item[0] for item in sorted_dic)
                fw.write('{}\t_\n'.format(key))
                not_print_key = False

            value = '\t'.join('{}'.format(item[1]) for item in sorted_dic)
            fw.write('{}\t_\n'.format(value))


def trim_distance(txt):
    m = distance_pat.search(txt)
    if m:
        return m.group(1)
    return txt


def lst_contains(src, lst):
    for item in lst:
        if item in src:
            return True
    return False


def split_floor(floor):
    m = floor_pat.search(floor)
    if m:
        return m.groups()
    return 0, 0


def custom_sort(dic):
    keys = ['id', 'title', 'price', 'size',
            'line', 'subway', 'subway_distance',
            'in_floor', 'floor', 'structure',
            'url', 'from_url', 'sub_title']
    sorted_lst = []

    for key in keys:
        sorted_lst.append((key, dic[key]))

    return sorted_lst


def main():
    process()


if __name__ == '__main__':
    main()

"""
更新租房的条件：
距离地铁必须近，10平米以上，朝南，3000以内。

租房的条件：
1. 价格不超过3500
2. 最好能够整租，合租最多两居室
3. 离地铁站越近越好，离市区越近越好
4. 最好是高楼层
5. 一定要是朝南的卧室
6，面积必须要大于10平米
"""
