#!/usr/bin/env python
# encoding: utf-8

"""
@description: 抽取数据

@author: baoqiang
@time: 2019-04-12 16:53
"""

import re

pat = re.compile('{Id:(\\d+) ')


def extract():
    with open('/Users/baoqiang/Downloads/2.txt', 'r', encoding='utf-8') as f:
        for line in f:
            m = pat.search(line)
            print(m.group(1))


def cmp():
    with open('/Users/baoqiang/Downloads/1.txt', 'r', encoding='utf-8') as f:
        a = set(f.readlines())

    with open('/Users/baoqiang/Downloads/2.txt', 'r', encoding='utf-8') as f:
        b = set(f.readlines())

    print(len(b), len(a))

    print(b - a)


if __name__ == '__main__':
    # extract()
    cmp()
