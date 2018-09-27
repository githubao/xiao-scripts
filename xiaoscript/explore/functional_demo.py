#!/usr/bin/env python
# encoding: utf-8

"""
@description: 函数式编程

@author: baoqiang
@time: 2018/9/27 下午1:34
"""

from random import random
from functools import reduce


def move_cars(car_positions):
    return map(lambda x: x + 1 if random() > 0.3 else x, car_positions)


def output_car(car_position):
    return '-' * car_position


def run_step_of_race(state):
    return {'time': state['time'] - 1, 'car_positions': move_cars(state['car_positions'])}


def draw(state):
    print('')
    print('\n'.join(map(output_car, state['car_positions'])))


def race(state):
    draw(state)
    if state['time']:
        race(run_step_of_race(state))


def run1():
    race({'time': 5, 'car_positions': [1, 1, 1]})


def even_filter(nums):
    for num in nums:
        if num % 2 == 0:
            yield num


def multi_by_three(nums):
    for num in nums:
        yield num * 3


def convert_to_string(nums):
    for num in nums:
        yield 'The number is: %s' % num


def run2():
    nums = range(1, 11)
    pipeline = convert_to_string(multi_by_three(even_filter(nums)))
    for num in pipeline:
        print(num)


def even_filter2(nums):
    return filter(lambda x: x % 2 == 0, nums)


def multi_by_three2(nums):
    return map(lambda x: x * 3, nums)


def convert_to_string2(nums):
    return map(lambda x: 'The number is: %s' % x, nums)


def run3():
    nums = range(1, 11)
    pipeline = convert_to_string2(multi_by_three2(even_filter2(nums)))
    for num in pipeline:
        print(num)


def pipeline_func(data, fns):
    return reduce(lambda a, x: x(a), fns, data)


def run4():
    nums = range(1, 11)
    pipeline = pipeline_func(nums, [even_filter2, multi_by_three2, convert_to_string2])
    for num in pipeline:
        print(num)


class Pipe(object):
    def __init__(self, func):
        self.func = func

    def __xor__(self, other):
        def generator():
            for obj in other:
                if obj is not None:
                    yield self.func(obj)

        return generator


@Pipe
def even_filter3(num):
    return num if num % 2 == 0 else None


@Pipe
def multiply_by_three3(num):
    return num * 3


@Pipe
def convert_to_string3(num):
    return 'The number is : %s' % num


@Pipe
def echo(item):
    print(item)
    return item


def force(sqs):
    for item in sqs:
        pass


def run5():
    nums = list(range(1, 11))
    force(nums | even_filter3 | multiply_by_three3 | convert_to_string3 | echo)


def run():
    # run1()
    # run2()
    # run3()
    # run4()
    run5()


if __name__ == '__main__':
    run()
