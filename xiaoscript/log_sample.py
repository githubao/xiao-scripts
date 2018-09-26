#!/usr/bin/env python
# encoding: utf-8

"""
@description: log的例子

@author: baoqiang
@time: 2018/9/26 下午7:58
"""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('test.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(levelname)s %(asctime)s - %(filename)s:%(lineno)d - %(message)s]')
handler.setFormatter(formatter)

logger.addHandler(handler)


def run_log():
    filename = '/path/to/does/not/exist'
    try:
        open(filename, 'r')
    except IOError as e:
        logger.error('failed to open file: {}'.format(filename), exc_info=True)


if __name__ == '__main__':
    run_log()
