#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: pacman
@time: 2018/2/13 11:13
"""

import requests
from collections import OrderedDict, defaultdict
import json
import sys
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

# out_file = 'C:\\Users\\xiaobao\\Desktop\\github.json'
out_file = '/mnt/home/baoqiang/github.json'

# ps_file = 'C:\\Users\\xiaobao\\Desktop\\1.txt'
ps_file = '/mnt/home/baoqiang/1.txt'

out_file2 = 'C:\\Users\\xiaobao\\Desktop\\github-lang.txt'

focus_keys = ['id', 'full_name', 'description', 'language', 'stargazers_count', 'forks_count', 'url', 'git_url']


def run():
    auth = get_auth()

    for i in range(1, 276):
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

        print('process cnt: {}'.format(i))
        sys.stdout.flush()


# url_fmt = 'https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&page={}&per_page=100'
url_fmt = 'https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&page={}&per_page=50'


def get_auth():
    # with open(ps_file, 'r', encoding='utf-8') as f:
    with open(ps_file, 'r', encoding='utf-8') as f:
        return f.read().strip().split(' ')


def count_lang():
    dic = defaultdict(int)

    with open(out_file, 'r', encoding='utf-8') as f, \
            open(out_file2, 'w', encoding='utf-8') as fw:
        for line in f:
            json_data = json.loads(line.strip())
            dic[json_data['language']] += 1

        sorted_dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)

        for item in sorted_dic:
            fw.write('{}\t{}\n'.format(item[0], item[1]))

    plt.bar(dic.values(), color='b', labels=dic.keys())
    plt.show()

    plt.pie(dic.values(), labels=dic.keys())
    plt.show()


def main():
    run()
    # count_lang()


if __name__ == '__main__':
    main()
