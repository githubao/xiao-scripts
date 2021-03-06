#!/usr/bin/env python
# encoding: utf-8

"""
@description: 去重

@author: baoqiang
@time: 2019/3/20 下午2:44
"""

from collections import defaultdict

afile = '/Users/baoqiang/Downloads/a.txt'
bfile = '/Users/baoqiang/Downloads/b.txt'
out_file = '/Users/baoqiang/Downloads/out.txt'

tmp_file = '/Users/baoqiang/Downloads/1.txt'


def count_sum():
    dic = defaultdict(int)

    with open(tmp_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            dic[line] += 1

    sorted_list = sorted(dic.items(), key=lambda x: x[1], reverse=True)

    for item, count in sorted_list:
        print(item, count)
    for item, count in sorted_list:
        print(item)


def dup2():
    """
    a文件是b文件的超集，找到在b文件中不存在的a的记录
    :return:
    """
    with open(afile, 'r', encoding='utf-8') as f:
        all_datas = set(item.strip() for item in f)

    with open(bfile, 'r', encoding='utf-8') as f:
        sub_datas = set(item.strip() for item in f)

    diff = all_datas - sub_datas

    with open(out_file, 'w', encoding='utf-8') as fw:
        for item in diff:
            fw.write('{}\n'.format(item))


def dup():
    with open(bfile, 'r', encoding='utf-8') as f:
        datas = set(item.strip() for item in f)

    with open(afile, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if line not in datas:
                print(line)


if __name__ == '__main__':
    dup2()
    # count_sum()
