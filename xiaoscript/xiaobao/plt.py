#!/usr/bin/env python
# encoding: utf-8

"""
@description: 折线图找出异常数据

@author: baoqiang
@time: 2018/10/9 下午3:06
"""

import matplotlib.pyplot as plt
from collections import OrderedDict


def plot():
    cnt = 0

    dic = get_data()

    for dt, datas in dic.items():
        X = [item[0][-2:] for item in datas]
        Y = [item[1] for item in datas]

        plt.title(dt)
        plt.plot(X, Y)
        plt.gca().set_ylim([0, max(Y) * 1.5])

        plt.show()

        # cnt += 1
        #
        # if cnt == 3:
        #     break


def get_data():
    key = ''
    dic = OrderedDict()

    with open('/Users/baoqiang/Downloads/1.txt', 'r') as f:
        for line in f:
            x, y = line.strip().split('\t')

            if not key:
                key = x
            if x.endswith('01'):
                key = x

            lst = dic.get(key, [])
            lst.append((x, int(y)))
            dic[key] = lst

    return dic


if __name__ == '__main__':
    plot()
