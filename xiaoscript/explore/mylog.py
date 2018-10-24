#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: baoqiang
@time: 2018/10/24 下午8:28
"""

import logging


def null_logger():
    logging.getLogger(__name__).addHandler(logging.NullHandler)

    logging.error('who %s am %d i %s', 'a', 333, '好的')


def file_logger():
    # create logger
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)

    # create file handler
    log_path = "./log.log"
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.WARN)

    # create formatter
    fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.error('this is wrong: %s', "barking")


if __name__ == '__main__':
    file_logger()
