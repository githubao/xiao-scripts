#!/usr/bin/env python
# encoding: utf-8

"""
@description: 统计golang里面引用的包

@author: baoqiang
@time: 2019-04-19 12:02
"""

import re
from collections import defaultdict

filename = '/Users/baoqiang/github.txt'

pats = [re.compile('(github.com/.*?/.*?)[/", #)]'),
        re.compile('(github.com/.*?/.*?)$')]


def count_sum():
    dic = defaultdict(int)

    with open(filename, 'r', encoding='utf-8') as f:
        success = 0

        for line in f:
            if '@github' in line:
                continue

            for pat in pats:
                m = pat.search(line)
                if m:
                    success += 1
                    dic[m.group(1)] += 1
                    break
            else:
                # print('err line: {}'.format(line.strip()))
                pass

    sorted_dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)

    print(success)

    for k, v in sorted_dic:
        print('{} -> {}'.format(k, v))
        # pass


if __name__ == '__main__':
    count_sum()
