#!/usr/bin/env python
# encoding: utf-8

"""
@description: json 保存文件数据

@author: pacman
@time: 2018/3/20 18:07
"""

import json

root_path = 'C:\\Users\\xiaobao\\Desktop\\telegram.json'


class JsonPipeline:
    def __init__(self):
        self.fw = open(root_path, 'a', encoding='utf-8')

    def process_item(self, item, spider):
        data = json.dumps(item, ensure_ascii=False, sort_keys=True)
        self.fw.write('{}\n'.format(data))

    def close_spider(self, spider):
        self.fw.close()
