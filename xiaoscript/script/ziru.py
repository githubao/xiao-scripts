#!/usr/bin/env python
# encoding: utf-8

"""
@description: 处理自如的爬虫数据，分析得到最应该租住的区域

@author: pacman
@time: 2018/3/2 17:29
"""

import json
from xiaoscript import config

root_path = config.get_root_path()


def process():
    not_print_key = True

    with open('{}/ziru.json'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/ziru.txt'.format(root_path), 'w', encoding='utf-8') as fw:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            json_data = json.loads(line.strip())

            sorted_dic = custom_sort(json_data)

            if not_print_key:
                key = '\t'.join(item[0] for item in sorted_dic)
                fw.write('{}\n'.format(key))
                not_print_key = False

            value = '\t'.join('{}'.format(item[1]) for item in sorted_dic)
            fw.write('{}\n'.format(value))


def custom_sort(dic):
    keys = ['id', 'title', 'price', 'size',
            'line', 'subway',
            'floor', 'structure',
            'url', 'from_url', 'sub_title']
    sorted_lst = []

    for key in keys:
        sorted_lst.append((key, dic[key]))

    return sorted_lst


def main():
    process()


if __name__ == '__main__':
    main()
