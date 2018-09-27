#!/usr/bin/env python
# encoding: utf-8

"""
@description: python2 和 python3 的一些不同

@author: baoqiang
@time: 2018/9/27 下午12:21
"""

from __future__ import print_function, division, generators
from __future__ import nested_scopes, absolute_import, with_statement

# from __future__ import unicode_literals

from platform import python_version
import sys


def run1():
    print(print_function)
    print(python_version())
    print(sys.version)
    print(sys.version_info)


def run2():
    """
    python2中，没有bytes类，unicode类类似于python3的str类，还有一个str类类似python3的bytes类

    python3中有str和bytes两种类型。str在内存中是通过unicode编码的

    :return:
    """

    a = '中文'
    b = a.encode('utf-8')

    print(b)
    print(type(a))
    print(type(b))

    c = b'\xe4\xb8\xad\xe6\x96\x87'
    d = c.decode('utf-8')
    print(d)
    print(type(c))
    print(type(d))


def run3():
    """
    理解python2的编解码

    str(bytes) 需要decode
    unicode(str) 需要encode

    :return:
    """

    a = '中文'
    b = a.decode('utf-8')

    print(a)
    print(b)
    print(type(a))
    print(type(b))

    c = u'中文'
    d = c.encode('utf-8')
    print(c)
    print(d)
    print(type(c))
    print(type(d))


def run():
    # run1()
    # run2()
    run3()


if __name__ == '__main__':
    run()
