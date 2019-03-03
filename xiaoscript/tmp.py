#!/usr/bin/env python
# encoding: utf-8

"""
@description: 测试

@author: pacman
@time: 2018/2/11 15:54
"""

import platform
import random

import re
import time

hanzi_pat = re.compile('[\u4e00-\u9fa5]')


def tmp():
    run_recom()


def run_recom():
    # token_re = re.compile("([€α%゜∮])([a-zA-Z0-9]{11})([a-f0-9XQZ])(\\1)", re.M)
    token_re = re.compile("([€α%゜∮])([a-zA-Z0-9]{11})([a-f0-9XQZ])([€α%゜∮])", re.M)
    s = '''你用过多闪不？我刚用了觉得蛮好玩的，来多闪加我呀~
【长按复制此暗号打开多闪即可加我】
∮JUr3z1yWDM11∮
我的ID ds666666'''
    # s = '∮DSrqAiBq77B9∮'
    m = token_re.search(s)
    if m:
        print(m.group())

def tmp9():
    """
    1744348368
    :return:
    """
    a = 1

    print(a == None)

    print(id(a))
    print(id(None))


def tmp8():
    # st = time.localtime(1350816710.8050799)
    st = time.localtime(time.time())
    print(time.strftime('%Y-%m-%d %H:%M:%S', st))
    print(time.strftime('%y-%m-%d %H:%M:%S', st))


def tmp7():
    for i in range(20):
        rand = random.random()
        print('{}: {:.3f}'.format(i + 1, rand))


def tmp6():
    a = [1, 2]
    # a[2] = 3
    print(a)


def tmp5():
    print(chr(0x9fa5 + 12))


def tmp4():
    """
    20902个汉字
    :return:
    """
    print(len(range(0x4e00, 0x9fa5 + 1)))

    with open('C:\\Users\\xiaobao\\Desktop\\1.txt', 'w', encoding='utf-8') as fw:
        for i in range(0x4e00, 0x9fa5 + 1):
            fw.write('{}\n'.format(chr(i)))


def tmp3():
    """
    小 -> 23567
    包 -> 21253
    :return:
    """
    # s = '包'
    # print(ord(s))
    #
    # i = 21253
    # print(chr(i))

    print(chr(65537))


def tmp2():
    """
    只是一个相同的字：我 292 KB -> 120 byte
    随机汉字 292 KB -> 216 KB
    :return:
    """

    with open('C:\\Users\\xiaobao\\Desktop\\1.txt', 'w', encoding='utf-8') as fw:
        for i in range(100000):
            rand = random.randint(0x4e00, 0x9fa5)
            fw.write(chr(rand))
        fw.write('\n')


def tmp1():
    print(platform.platform())


def main():
    tmp()


if __name__ == '__main__':
    main()
