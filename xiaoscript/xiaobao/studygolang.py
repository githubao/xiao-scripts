#!/usr/bin/env python
# encoding: utf-8

"""
@description: studygolang的文章，一天产出10篇，出现的数据不再读取

@author: baoqiang
@time: 2019/2/27 下午8:46
"""

import random
from datetime import datetime
import sys

article_fmt = 'https://studygolang.com/articles/{}'

count = 10
total = 18500
# total = 23

if len(sys.argv) > 1:
    count = int(sys.argv[1])


def randit():
    with open('../data/studygolang.txt', 'r') as f:
        exists = set(int(line.strip()) for line in f.readlines())

    results = set()

    while True:
        if len(results) + len(exists) >= total:
            break

        random.seed(datetime.now())
        n = random.randint(1, total)
        if n not in exists:
            results.add(n)

        if len(results) >= count:
            break

    with open('../data/studygolang.txt', 'a') as fw:
        for item in results:
            fw.write('{}\n'.format(item))

    for item in results:
        print(article_fmt.format(item))


if __name__ == '__main__':
    randit()
