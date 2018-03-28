#!/usr/bin/env python
# encoding: utf-8

"""
@description: 写成示例

@author: pacman
@time: 2018/3/28 12:28
"""

import asyncio
import random


@asyncio.coroutine
def fib_smart(n):
    idx = 0
    a = 0
    b = 1
    while idx < n:
        time_consuming_task = random.uniform(0, 0.2)
        yield from asyncio.sleep(time_consuming_task)
        print('Smart one think {:.3f} secs to get {}'.format(time_consuming_task, b))
        a, b = b, a + b
        idx += 1


@asyncio.coroutine
def fib_stupid(n):
    idx = 0
    a = 0
    b = 1
    while idx < n:
        time_consuming_task = random.uniform(0, 0.4)
        yield from asyncio.sleep(time_consuming_task)
        print('Stupid one think {:.3f} secs to get {}'.format(time_consuming_task, b))
        a, b = b, a + b
        idx += 1


async def fib_smart2(n):
    idx = 0
    a = 0
    b = 1
    while idx < n:
        time_consuming_task = random.uniform(0, 0.2)
        await asyncio.sleep(time_consuming_task)
        print('Smart one think {:.3f} secs to get {}'.format(time_consuming_task, b))
        a, b = b, a + b
        idx += 1

    return 'from smart'


async def fib_stupid2(n):
    idx = 0
    a = 0
    b = 1
    while idx < n:
        time_consuming_task = random.uniform(0, 0.4)
        await asyncio.sleep(time_consuming_task)
        print('Stupid one think {:.3f} secs to get {}'.format(time_consuming_task, b))
        a, b = b, a + b
        idx += 1

    return 'from stupid'


def run():
    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.async(fib_smart2(10)),
        asyncio.async(fib_stupid2(10))
    ]

    results = loop.run_until_complete(asyncio.wait(tasks))
    for item in results[0]:
        print(item.get_result())

    print('all tasks finished')

    loop.close()


def main():
    run()


if __name__ == '__main__':
    main()
