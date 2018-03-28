#!/usr/bin/env python
# encoding: utf-8

"""
@description: 我的写成程序的实现

@author: pacman
@time: 2018/3/28 11:46
"""


def fib_norm(n):
    res = [0] * n
    idx = 0
    a = 0
    b = 1
    while idx < n:
        res[idx] = b
        a, b = b, a + b
        idx += 1
    return res


def fib_yield(n):
    idx = 0
    a = 0
    b = 1
    while idx < n:
        yield b
        a, b = b, a + b
        idx += 1


def fib_send(n):
    idx = 0
    a = 0
    b = 1
    while idx < n:
        sign = yield b
        print('received: {}'.format(sign))
        a, b = b, a + b
        idx += 1


def run1():
    for num in fib_norm(10):
        print(num)


def run2():
    for num in fib_yield(10):
        print(num)


def run3():
    fib = fib_send(10)

    # 下面这两句是等价的
    # res = next(fib)  # 获取到第一次yield的值
    res = fib.send(None)
    i = 1

    while True:
        print(res)

        try:
            res = fib.send('hello-{}'.format(i))
        except StopIteration:
            break

        i += 1


def main():
    # run1()
    # run2()
    run3()


if __name__ == '__main__':
    main()
