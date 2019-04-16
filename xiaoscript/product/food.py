#!/usr/bin/env python
# encoding: utf-8

"""
@description: 统计美食的数量

@author: baoqiang
@time: 2019/3/19 下午1:01
"""

import re
from collections import defaultdict

regex = re.compile(' (.*)-(.*): (\d+)')


def count_sum():
    filename = '/Users/baoqiang/Downloads/eating.txt'

    counts = defaultdict(int)

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            m = regex.search(line)
            if m:
                text = m.group(2)

                try:
                    idx = text.index('(')
                except ValueError:
                    idx = -1

                if idx >= 0:
                    text = text[:idx]

                cnt = int(m.group(3))

                counts[text] += cnt

    sorted_dic = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    cnt = 0
    for k, v in sorted_dic:
        # if v == 1:
        #     break

        cnt += 1
        if cnt > 500:
            break

        print('{} -> {}'.format(k, v))


if __name__ == '__main__':
    count_sum()
