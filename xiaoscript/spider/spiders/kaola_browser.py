#!/usr/bin/env python
# encoding: utf-8

"""
@description: 无头浏览器

@author: baoqiang
@time: 2019-05-15 21:32
"""

from selenium import webdriver
from scrapy.selector import Selector

start_url = 'https://www.kaola.com'


def crawl():
    driver = webdriver.PhantomJS()
    driver.get(start_url)

    # resp = driver.find_element_by_xpath('.//div[@class="litd"]//a[@class="cat2"]')
    # print(resp)

    print(driver.title)

    # doc = Selector(root=resp)


if __name__ == '__main__':
    crawl()
