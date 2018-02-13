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
import time
import random
import platform

plt.rcParams['font.sans-serif'] = ['SimHei']

out_file = '/mnt/home/baoqiang/github.json'
ps_file = '/mnt/home/baoqiang/1.txt'

if 'Windows' in platform.platform():
    ps_file = 'C:\\Users\\xiaobao\\Desktop\\1.txt'
    out_file = 'C:\\Users\\xiaobao\\Desktop\\github.json'

out_file2 = 'C:\\Users\\xiaobao\\Desktop\\github-lang.txt'

focus_keys = ['id', 'full_name', 'description', 'language', 'stargazers_count', 'forks_count', 'url', 'git_url']

start = 1000
step = 50
end = 7850


def run():
    auth = get_auth()

    # 保存所有请求回来的json
    dic_list = []

    # 先star > 7850 的json
    for i in range(1, 21):
        json_data = req(url_fmt2.format(i), auth)
        dic_list.append(json_data)

        print('process large num cnt: {}'.format(i))
        sys.stdout.flush()

    for i in range(start, end, step):
        # 第一次请求
        json_data = req(url_fmt.format(i, i + step, 1), auth)
        dic_list.append(json_data)

        # 后续的请求
        pg_num = get_pg_num(json_data['total_count'])
        if pg_num > 2:
            for j in range(2, pg_num):
                json_data2 = req(url_fmt.format(i, i + step, j), auth)
                dic_list.append(json_data2)

                # break

        print('process batch cnt: {}'.format(i))
        sys.stdout.flush()

    # 保存数据
    result_dic = {}
    for json_data in dic_list:
        for item in json_data['items']:
            dic = OrderedDict()
            for key in focus_keys:
                dic[key] = item[key]

            result_dic[dic['id']] = dic

    # 排序
    sorted_dic = sorted(result_dic.items(), key=lambda x: x[1]['stargazers_count'], reverse=True)

    with open(out_file, 'a', encoding='utf-8') as fw:
        for item in sorted_dic:
            json.dump(item[1], fw, ensure_ascii=False)
            fw.write('\n')


def get_pg_num(count):
    int_num = int(count / step)
    float_num = count / step

    if int_num == float_num:
        return int_num + 1
    else:
        return int_num + 2


def req(url, auth):
    response = requests.get(url, auth=tuple(auth))
    time.sleep(random.random() * 3)
    return response.json()


url_fmt2 = 'https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&page={}&per_page=50'

url_fmt = 'https://api.github.com/search/repositories?q=stars:{}..{}&sort=stars&order=desc&page={}&per_page=50'


def get_auth():
    # with open(ps_file, 'r', encoding='utf-8') as f:
    with open(ps_file, 'r', encoding='utf-8') as f:
        return f.read().strip().split(' ')


def count_lang():
    dic = defaultdict(int)

    with open(out_file, 'r', encoding='utf-8') as f:
        for line in f:
            json_data = json.loads(line.strip())
            dic[json_data['language']] += 1

    # 整理dic,把小于1%的统一为other
    dic = norm_dic(dic)

    # plt.bar(range(len(dic)), dic.values(), color='b', tick_label=dic.keys())
    # plt.show()

    plt.pie(dic.values(), labels=get_labels(dic))
    plt.title("Github网站star>=1000的项目使用语言占比饼状图\n")
    plt.axis('equal')
    plt.show()


def norm_dic(dic):
    total_cnt = sum(dic.values())

    updated_dic = {}

    other_cnt = 0
    other_lst = []
    for lang, cnt in dic.items():
        if cnt / total_cnt <= 0.01:
            other_cnt += cnt
            other_lst.append(lang)
        else:
            updated_dic[lang] = cnt

    other_key = ','.join(other_lst)
    print('Other: {}'.format(other_key))
    updated_dic['Other'] = other_cnt

    sorted_lst = sorted(updated_dic.items(), key=lambda x: x[1], reverse=True)

    sorted_dic = OrderedDict()

    total = sum(dic.values())
    for item in sorted_lst:
        sorted_dic[item[0]] = item[1]
        # print('{}:{:.2f}%'.format(item[0], item[1] / total * 100))

    return updated_dic


def get_labels(dic):
    percent_lst = []
    total = sum(dic.values())
    for key, value in dic.items():
        fmt = '{}({:.2f}%)'.format(key, value / total * 100)
        percent_lst.append(fmt)

    return percent_lst


def main():
    # run()
    count_lang()


if __name__ == '__main__':
    main()
