#!/usr/bin/env python
# encoding: utf-8

"""
@description: 命令行中运行爬虫

@author: pacman
@time: 2018/2/9 17:35
"""

from scrapy import cmdline


def run():
    # cmdline.execute('scrapy crawl wandou2'.split())
    # cmdline.execute('scrapy crawl wandou'.split())
    # cmdline.execute('scrapy crawl jike'.split())
    # cmdline.execute('scrapy crawl ziru'.split())
    # cmdline.execute('scrapy crawl ziru2'.split())
    # cmdline.execute('scrapy crawl nuanfang'.split())
    # cmdline.execute('scrapy crawl danke'.split())
    # cmdline.execute('scrapy crawl miui'.split())
    cmdline.execute('scrapy crawl lianjia2'.split())
    # cmdline.execute('scrapy crawl dianping'.split())
    # cmdline.execute('scrapy crawl telegram'.split())
    # cmdline.execute('scrapy crawl studygo'.split())
    # cmdline.execute('scrapy crawl cool_shell'.split())
    # cmdline.execute('scrapy crawl trip_advisor'.split())
    # cmdline.execute('scrapy crawl kaola'.split())
    # cmdline.execute('scrapy crawl jianshu_collection'.split())


def main():
    run()


if __name__ == '__main__':
    main()
