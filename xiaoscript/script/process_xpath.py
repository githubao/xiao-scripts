#!/usr/bin/env python
# encoding: utf-8

"""
@description: 处理xpath文件

@author: pacman
@time: 2018/1/30 11:00
"""

from scrapy.selector import Selector
import re

num_pat = re.compile('[\d]+')

root_path = 'C:\\Users\\xiaobao\\Desktop'


def process():
    with open('{}\{}'.format(root_path, '1.html'), 'r', encoding='utf-8') as f, \
            open('{}\{}'.format(root_path, '1.txt'), 'w', encoding='utf-8') as fw:

        html = f.read()
        root = Selector(text=html)

        classes = root.xpath('//tbody//td[@align="center"]')
        for item in classes:
            text = item.xpath('.//text()')[0].extract().strip()

            m = num_pat.match(text)
            if m:
                continue

            fw.write('{}\n'.format(text))


def example():
    html = open("C:\\Users\\BaoQiang\\Desktop\\1.html", 'r', encoding='utf-8').read()
    root = Selector(text=html)

    doc_answers = root.xpath('//div[contains(@class,"Doc_con")]/div[contains(@class,"docall")]')
    answers = []
    for doc_answer in doc_answers:
        answer = {}
        all_answers = doc_answer.xpath('.//div[contains(@class,"qsdetail")]//div[contains(@class,"pt15")]/text()')
        answer_list = [item.extract().strip() for item in all_answers]
        answer['answer'] = '。'.join(answer_list)

        answers.append(answer)


def main():
    process()


if __name__ == '__main__':
    main()
