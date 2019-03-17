#!/usr/bin/env python
# encoding: utf-8

"""
@description: 翻译

@author: baoqiang
@time: 2019/3/17 下午5:12
"""

import requests

url_fmt = 'http://fy.iciba.com/ajax.php?a=fy&f=auto&t=auto&w={}'


def translate(word):
    if not word:
        return ''

    resp = requests.get(url_fmt.format(word))

    jdata = resp.json()

    res = ''

    if jdata['status'] == 0:
        res = ' '.join(jdata['content']['word_mean'])
    elif jdata['status'] == 1:
        content = jdata['content']
        if content['err_no'] == 0:
            res = content['out']

    if not res:
        print('err: {}'.format(jdata))

    return res
