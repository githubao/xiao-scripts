#!/usr/bin/env python
# encoding: utf-8

"""
@description: 命令行中运行爬虫

@author: pacman
@time: 2018/2/9 17:35
"""

from scrapy import cmdline


def run():
    cmdline.execute('scrapy crawl lianjia'.split())


def main():
    run()


if __name__ == '__main__':
    main()
