#!/usr/bin/env python
# encoding: utf-8

"""
@description: 通用配置

@author: pacman
@time: 2018/3/2 17:20
"""

import platform


def get_root_path():
    plt = platform.platform()

    root_path = ''
    if 'Linux' in plt:
        root_path = '/mnt/home/baoqiang'
    elif 'Windows' in plt:
        root_path = 'C:\\Users\\xiaobao\\Desktop'
    elif 'Darwin' in plt:
        root_path = '/Users/baoqiang/Downloads'

    return root_path
