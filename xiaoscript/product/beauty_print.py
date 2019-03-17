#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: baoqiang
@time: 2019/3/17 下午5:46
"""


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def fill_text_to_print_width(text, width):
    # stext = str(text)
    # utext = stext.decode("utf-8")
    cn_count = 0
    for u in text:
        if is_chinese(u):
            cn_count += 1
    return text + (" " * (width - cn_count - len(text)))


