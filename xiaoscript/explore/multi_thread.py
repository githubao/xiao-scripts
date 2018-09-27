#!/usr/bin/env python
# encoding: utf-8

"""
@description: 多线程示例程序

@author: baoqiang
@time: 2018/9/27 上午11:49
"""

import threading
import time

mutex = threading.Lock()


def write_file(filename):
    mutex.acquire()

    thread_name = threading.current_thread().getName()

    with open(filename, 'a') as fw:
        print('Thread {} acquire lock'.format(thread_name))
        fw.write('write from thread {}\n'.format(thread_name))

        time.sleep(1)

    print('Thread {} exit'.format(thread_name))

    mutex.release()


def run():
    threads = []

    for i in range(5):
        t = threading.Thread(target=write_file, args=('threading.txt',))
        threads.append(t)

    for i in range(5)[::-1]:
        threads[i].start()

    for i in range(5):
        threads[i].join()


if __name__ == '__main__':
    run()
