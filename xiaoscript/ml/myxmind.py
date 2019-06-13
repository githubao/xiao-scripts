#!/usr/bin/env python
# encoding: utf-8

"""
@description: 使用python生成思维导图

@author: baoqiang
@time: 2019-06-12 18:28
"""

import xmind
import os
import json
from collections import OrderedDict

json_file = os.path.join(os.environ['HOME'], 'Downloads', 'pca.json')

root_path = os.path.join(os.environ['HOME'], 'Downloads', 'china')


# https://pypi.org/project/XMind/
def gen_my_xmind_file():
    with open(json_file, 'rt') as f:
        jdata = json.loads(f.read(), object_pairs_hook=OrderedDict)

    for k1, v1 in jdata.items():
        xmind_file = os.path.join(root_path, "{}.xmind".format(k1))
        workbook = xmind.load(xmind_file)
        sheet1 = workbook.getPrimarySheet()
        design_sheet1(sheet1, k1, v1)

        xmind.save(workbook)


def design_sheet1(sheet1, k, v):
    sheet1.setTitle(k)  # 设置画布名称

    # 获取画布的中心主题，默认创建画布时会新建一个空白中心主题
    root = sheet1.getRootTopic()
    root.setTitle(k)  # 设置主题名称

    cnt = 0
    for k1, v1 in v.items():
        cnt += 1
        sub1 = root.addSubTopic()
        sub1.setTitle('{}. {}'.format(cnt, k1))
        for v2 in v1:
            sub2 = sub1.addSubTopic()
            sub2.setTitle(v2)
        sub1.setFolded()


def run():
    gen_my_xmind_file()


if __name__ == '__main__':
    run()
