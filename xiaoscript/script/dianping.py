#!/usr/bin/env python
# encoding: utf-8

"""
@description: 按照地铁线评价数量排序的最多的20家店，而且评价数需要超过1000才打印

@author: pacman
@time: 2018/2/12 11:44
"""

import json

root_path = 'C:\\Users\\xiaobao\\Desktop\\'


def run():
    with open('{}/dianping.json'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/dianping.txt'.format(root_path), 'w', encoding='utf-8') as fw:
        for line in f:
            line = line.strip()


def main():
    print('do sth')


if __name__ == '__main__':
    main()
