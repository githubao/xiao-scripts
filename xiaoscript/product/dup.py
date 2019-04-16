#!/usr/bin/env python
# encoding: utf-8

"""
@description: 去重

@author: baoqiang
@time: 2019/3/20 下午2:44
"""

afile = '/Users/baoqiang/Downloads/a.txt'
bfile = '/Users/baoqiang/Downloads/b.txt'


def dup():
    with open(bfile, 'r', encoding='utf-8') as f:
        datas = set(item.strip() for item in f)

    with open(afile, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if line not in datas:
                print(line)


if __name__ == '__main__':
    dup()
