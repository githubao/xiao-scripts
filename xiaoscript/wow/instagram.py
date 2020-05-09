#!/usr/bin/env python
# encoding: utf-8

"""
@description: 解析下载到的文件名

@author: baoqiang
@time: 2020/4/15 11:40 上午
"""

import re

filename = '2020-04-11_03-32-59_UTC_B-01w36lbAR_s_ylll_1.jpg'
pat_str = '([\\d_-]{19})_UTC_([\\d\\w-]{11})_([\\w_]+?)_(\\d{1,2})?\\.jpg'
pat = re.compile(pat_str)


def match():
    m = pat.match(filename)
    if not m:
        print('un match: {}'.format(filename))
        return

    print('user:{}, link:{}, time:{}'.format(link_user(m[3]), link_post(m[2]), m[1]))


def link_user(u):
    return 'https://www.instagram.com/{}/'.format(u)


def link_post(p):
    return 'https://www.instagram.com/p/{}/'.format(p)


if __name__ == '__main__':
    match()
