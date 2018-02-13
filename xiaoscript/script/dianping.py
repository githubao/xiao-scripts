#!/usr/bin/env python
# encoding: utf-8

"""
@description: 按照地铁线评价数量排序的最多的20家店，而且评价数需要超过1000才打印

@author: pacman
@time: 2018/2/12 11:44
"""

import json
from collections import defaultdict
import traceback

root_path = 'C:\\Users\\xiaobao\\Desktop\\'


def run():
    dic = defaultdict(dict)

    with open('{}/dianping.json'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/北京美食地图(地铁线).md'.format(root_path), 'w', encoding='utf-8') as fw:
        for line in f:
            line = line.strip()
            json_data = json.loads(line)

            if 'comment_cnt' not in json_data or '￥' in '{}'.format(json_data['comment_cnt']):
                continue

            try:
                subline = json_data['line']
                station = json_data['station']
                name = json_data['name']
                cnt = int(json_data['comment_cnt'])
                url = json_data['url']
                tag = json_data['tag'] if 'tag' in json_data else ' '

                if station not in dic[subline]:
                    dic[subline][station] = {}

                dic[subline][station][name] = [url, cnt, tag]
            except Exception as e:
                traceback.print_exc()
                print(line)

        fw.write('## 北京美食地图(地铁线)\n')
        for line, line_val in dic.items():
            fw.write('### {}\n'.format(line))

            for station, station_val in line_val.items():
                fw.write('#### {}\n'.format(station))

                sorted_dic = sorted(station_val.items(), key=lambda x: x[1][1], reverse=True)

                for item in sorted_dic:
                    if item[1][1] < 1000:
                        break

                    fw.write('1. {}-[{}]({}): {}\n'.format(item[1][2], item[0], item[1][0], item[1][1]))


def run2():
    dic = {}

    with open('{}/dianping.json'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/北京美食地图(好评数).md'.format(root_path), 'w', encoding='utf-8') as fw:
        for line in f:
            line = line.strip()
            json_data = json.loads(line)

            if 'comment_cnt' not in json_data or '￥' in '{}'.format(json_data['comment_cnt']):
                continue

            subline = json_data['line']
            station = json_data['station']
            name = json_data['name']
            cnt = int(json_data['comment_cnt'])
            url = json_data['url']
            tag = json_data['tag'] if 'tag' in json_data else ' '

            dic[name] = [subline, station, cnt, url, tag]

        sorted_lst = sorted(dic.items(), key=lambda x: x[1][2], reverse=True)

        fw.write('## 北京美食地图(好评数)\n')
        for name, items in sorted_lst:
            if items[2] >= 1000:
                fw.write('1. {}-{} {}-[{}]({}): {}\n'.format(items[0], items[1], items[4], name, items[3], items[2]))


def main():
    run()
    run2()


if __name__ == '__main__':
    main()
