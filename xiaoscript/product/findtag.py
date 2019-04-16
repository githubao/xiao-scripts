#!/usr/bin/env python
# encoding: utf-8

"""
@description: 统计找到不包含F,W的列还有没有其他的值

@author: baoqiang
@time: 2019/3/26 下午6:11
"""

from collections import defaultdict

filename = '/Users/baoqiang/Downloads/type.txt'
outname = '/Users/baoqiang/Downloads/type_out.txt'


def find():
    dic = defaultdict(list)

    tagdic = {}

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            mobile, tag = line.strip().split('\t')
            dic[mobile].append(tag)

    for mobile, tags in dic.items():
        ok = False

        for tag in tags:
            if tag in ['F', 'W']:
                continue
            else:
                ok = True
                break

        if ok:
            tagdic[mobile] = True
        else:
            tagdic[mobile] = False

    # write data
    with open(filename, 'r', encoding='utf-8') as f, \
            open(outname, 'w', encoding='utf-8') as fw:

        for line in f:
            mobile, tag = line.strip().split('\t')
            ok = tagdic[mobile]

            if ok:
                fw.write('{}\t{}\n'.format(mobile, 1))
            else:
                fw.write('{}\t{}\n'.format(mobile, 0))


if __name__ == '__main__':
    find()
