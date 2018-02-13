#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: pacman
@time: 2018/2/13 11:13
"""

import requests
from collections import OrderedDict
import json

out_file = '/mnt/home/baoqiang/github.json'
# out_file = 'C:\\Users\\xiaobao\\Desktop\\github.json'

focus_keys = ['id', 'full_name', 'description', 'language', 'stargazers_count', 'forks_count', 'url', 'git_url']


def run():
    auth = get_auth()

    # for i in range(1, 3):
    for i in range(1, 139):
        response = requests.get(url_fmt.format(i), auth=tuple(auth))
        json_data = response.json()

        results = []
        for item in json_data['items']:
            dic = OrderedDict()
            for key in focus_keys:
                dic[key] = item[key]

            results.append(dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False)
                fw.write('\n')


url_fmt = 'https://api.github.com/search/repositories?sort=stars&order=desc&per_page=100&page=0&q=stars:>1000'


def get_auth():
    # with open('C:\\Users\\xiaobao\\Desktop\\1.txt', 'r', encoding='utf-8') as f:
    with open('/mnt/home/baoqiang/1.txt', 'r', encoding='utf-8') as f:
        return f.read().strip().split(' ')


def main():
    run()


if __name__ == '__main__':
    main()
