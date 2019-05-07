#!/usr/bin/env python
# encoding: utf-8

"""
@description: 检测一张图片是不是全黑色

@author: baoqiang
@time: 2019-04-23 18:50
"""

from PIL import Image
import pandas as pd
import requests

filename = '/Users/baoqiang/Downloads/1.txt'
out_filename = '/Users/baoqiang/Downloads/out.txt'
out2_filename = '/Users/baoqiang/Downloads/out2.txt'

pic_path = '/Users/baoqiang/Downloads/pics'


def judge_black():
    df = pd.read_csv(filename)

    fw = open(out_filename, 'w')

    for idx, item in enumerate(df.iterrows(), start=1):
        # print(item[1][0], item[1][1], item[1][2])

        mid = item[1][0]
        aid = item[1][1]
        pic_url = item[1][2]

        try:
            pic_file = download_pic(pic_url)

            black = is_black(pic_file)
        except Exception as e:
            print('{}\t{}\n'.format(mid, e))
            continue

        fw.write('{}\t{}\t{}\t{}\n'.format(mid, aid, pic_url, black))

        if idx % 100 == 0:
            print('process [{}] cnt: {}'.format(pic_file, idx))

    fw.close()


def download_pic(pic_url):
    if not pic_url:
        return

    resp = requests.get(pic_url)
    pic_id = pic_url.split('/')[-1]
    pic_file = '{}/{}.jpg'.format(pic_path, pic_id)

    with open(pic_file, 'wb') as fw:
        fw.write(resp.content)

    return pic_file


def is_black(image_file):
    img = Image.open(image_file)
    if not img.getbbox():
        return 1
    else:
        return 0


def is_black2(image_file):
    if not image_file:
        return 1

    img = Image.open(image_file)
    extrema = img.convert("L").getextrema()
    # if extrema[0] == extrema[1] and extrema[0] == 0:
    #     return 1
    # else:
    #     return 0
    # if extrema[0] < 5 and extrema[1] < 5:
    if extrema[0] < 10 and extrema[1] < 10:
        return 1
    else:
        return 0


def process_black():
    with open(out_filename, 'r', encoding='utf-8') as f, \
            open(out2_filename, 'w', encoding='utf-8') as fw:
        for idx, line in enumerate(f, start=1):

            line = line.strip()
            attrs = line.split('\t')

            try:
                if len(attrs) > 1:
                    pic_url = attrs[1]
                else:
                    pic_url = ""

                pic_file = download_pic(pic_url)
                # pic_file = ""
            except Exception as e:
                print("processing failed: {}, {}".format(line,e))
                pic_file = ''

            if is_black2(pic_file):
                ok = 1
            else:
                ok = 0

            fw.write('{}\t{}\t{}\n'.format(attrs[0], pic_url, ok))

            if idx % 100 == 0:
                print('process cnt: {}'.format(idx))


def run_hello():
    pic_file = '/Users/baoqiang/Downloads/pics/1d1e7000646931e3a9767.jpg'
    print(is_black(pic_file))
    print(is_black2(pic_file))


if __name__ == '__main__':
    # judge_black()
    # run_hello()
    process_black()
