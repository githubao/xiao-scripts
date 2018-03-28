#!/usr/bin/env python
# encoding: utf-8

"""
@description: 测试Python GLI的存在

CPU密集型的计算任务，没有效果
IO密集型的任务，其实时间主要是在文件读写，跟CPU计算没有关系。只要把一行连接的代码执行了就好了。。。阻塞并发执行，所以多线程会提高效率

@author: pacman
@time: 2018/3/28 11:25
"""

import time
import functools
import threading


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.clock()
        res = func(*args, **kwargs)
        end = time.clock()
        print('{} time: {:.3f}'.format(func.__name__, (end - start)))
        return res

    return wrapper


def my_counter():
    i = 0
    for _ in range(100000000):
        i += 1


@timeit
def single_thread():
    for _ in range(3):
        t = threading.Thread(target=my_counter)
        t.start()
        t.join()


@timeit
def multi_thread():
    t_arr = []
    for i in range(3):
        t = threading.Thread(target=my_counter)
        t_arr.append(t)
        t.start()

    for i in range(3):
        t_arr[i].join()


def main():
    """
    single_thread time: 21.785
    multi_thread time: 22.813
    :return:
    """
    single_thread()
    multi_thread()


if __name__ == '__main__':
    main()
