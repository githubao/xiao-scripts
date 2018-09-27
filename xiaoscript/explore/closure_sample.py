#!/usr/bin/env python
# encoding: utf-8

"""
@description: 闭包的例子
函数外面（全局作用域）可以知道函数里面的局部变量的值

@author: baoqiang
@time: 2018/9/27 下午12:02
"""


def add_n(n):
    def wrapper(a):
        i = 1
        return i + a + n

    return wrapper


def closure_run():
    add_3 = add_n(3)
    res = add_3(5)
    print(res)


if __name__ == '__main__':
    closure_run()
