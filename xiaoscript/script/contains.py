#!/usr/bin/env python
# encoding: utf-8

"""
@description: 判断一个文件中的数据，另一个文件是否包含，相当于excel的vlookup

@author: pacman
@time: 2017/11/28 22:22
"""

import sys

root_path = 'C:\\Users\\xiaobao\\Desktop\\'

item_count = 2


def run():
    with open('{}/to-contain.txt'.format(root_path), 'r', encoding='utf-8') as f:
        keywords = set(item.strip() for item in f)

    with open('{}/source.txt'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/result.txt'.format(root_path), 'w', encoding='utf-8') as fw:
        for idx, line in enumerate(f, start=1):
            line = line.strip()

            items = line.split('\t')

            if len(items) != item_count:
                continue

            key = items[0]
            if key in keywords:
                fw.write('{}\n'.format(line))

            if idx % 1000 == 0:
                print('process cnt: {}'.format(idx))
                sys.stdout.flush()


def main():
    run()


if __name__ == '__main__':
    main()
