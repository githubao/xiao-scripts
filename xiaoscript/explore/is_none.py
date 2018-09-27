#!/usr/bin/env python
# encoding: utf-8

"""
@description: python的is 和 none

@author: baoqiang
@time: 2018/9/27 下午12:11
"""


def run():
    a = None
    print(a is None)
    print(a == None)
    print(id(None))
    print(id(a))


def run2():
    a = []
    cmp(a)


def cmp(a):
    b = []
    print(a == b)
    print(a is b)
    print(id(a))
    print(id(b))


if __name__ == '__main__':
    # run()
    run2()
