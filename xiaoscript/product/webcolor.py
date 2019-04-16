#!/usr/bin/env python
# encoding: utf-8

"""
@description: rgb 和 颜色 的转化

@author: baoqiang
@time: 2019/3/17 下午4:51
"""

import sys

import webcolors
from sty import fg

sys.path.append('/Users/baoqiang/xiao/python_repos/xiao-scripts')

try:
    from xiaoscript.product.translate import translate
    from xiaoscript.product.beauty_print import fill_text_to_print_width
except ImportError:
    raise

line_hex = {
    "1号线": "#A4343A",
    "八通线": "#A4343A",
    "2号线": "#004B87",
    "4号线": "#008C95",
    "大兴线": "#008C95",
    "5号线": "#AA0061",
    "6号线": "#B58500",
    "7号线": "#FFC56E",
    "8号线": "#009B77",
    "9号线": "#97D700",
    "10号线": "#0092BC",
    "13号线": "#F4DA40",
    "14号线": "#CA9A8E",
    "15号线": "#653279",
    "16号线": "#6BA539",
    "亦庄线": "#D0006F",
    "房山线": "#D86018",
    "燕房线": "#D86018",
    "S1线": "#A45A2A",
    "昌平线": "#D986BA",
    "西郊线": "#D22630",
    "机场线": "#A192B2",
}

line_color = {
    "1号线": "正红色",
    "八通线": "正红色",
    "2号线": "蓝色",
    "4号线": "青绿色",
    "大兴线": "青绿色",
    "5号线": "紫色",
    "6号线": "土黄色",
    "7号线": "淡黄色",
    "8号线": "深绿色",
    "9号线": "淡绿色",
    "10号线": "天蓝色",
    "13号线": "藤黄色",
    "14号线": "淡粉色",
    "15号线": "紫罗兰色",
    "16号线": "草绿色",
    "亦庄线": "桃红色",
    "房山线": "橙红色",
    "燕房线": "橙红色",
    "S1线": "棕色",
    "昌平线": "嫩粉色",
    "西郊线": "朱红色",
    "机场线": "银灰色",
}


def colored():
    for line, hex_ in line_hex.items():
        r, g, b = hex2rgb(hex_)

        # r, g, b = (255, 10, 10)

        fmt = fill_text_to_print_width(line, 6)
        src = '{}\t| {} |{}'.format(fg(r, g, b), fmt, fg.rs)

        print(src)


def convert():
    for line, hex_ in line_hex.items():
        # name = webcolors.hex_to_name(rgb)

        rgb = hex2rgb(hex_)

        _, closest = get_colour_name(rgb)

        chinese = translate(closest)

        print('{} -> {}, {}'.format(line, closest, chinese))


def hex2rgb(src):
    r, g, b = webcolors.hex_to_rgb(src)
    return r, g, b


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


# requested_colour = (119, 172, 152)
# actual_name, closest_name = get_colour_name(requested_colour)
# print("Actual colour name:", actual_name, ", closest colour name:", closest_name)

if __name__ == '__main__':
    # convert()
    colored()
