#!/usr/bin/env python
# encoding: utf-8

"""
@description: python 画图

@author: pacman
@time: 2018/4/2 11:11
"""

import os
import matplotlib.pyplot as plt
import numpy as np

out_path = 'C:\\Users\\xiaobao\\Desktop\\'


# 堆叠柱状图
def stacked_histogram():
    x = [1, 2, 3]
    y1 = np.array([2, 3, 2])
    y2 = np.array([3, 1, 5])
    y3 = np.array([1, 2, 1])

    # plt.bar(x, y1, color='green', label='y1')
    # plt.bar(x, y2, bottom=y1, color='red', label='y2')
    # plt.bar(x, y3, bottom=y1 + y2, color='blue', label='y3')

    plt.barh(x, y1, color='green', label='y1')
    plt.barh(x, y2, left=y1, color='red', label='y2')
    plt.barh(x, y3, left=y1 + y2, color='blue', label='y3')

    plt.legend(loc=[1, 0])

    full_file = os.path.join(out_path, '1.png')
    plt.savefig(full_file)

    plt.show()


def run():
    stacked_histogram()


def main():
    run()


if __name__ == '__main__':
    main()
