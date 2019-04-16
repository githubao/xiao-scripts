#!/usr/bin/env python
# encoding: utf-8

"""
@description: 获取图片的拍摄信息

@author: baoqiang
@time: 2019-04-03 15:01
"""

import os
import exifread


def getExif(filename):
    FIELD = 'EXIF DateTimeOriginal'
    fd = open(filename, 'rb')
    tags = exifread.process_file(fd)
    fd.close()
    # 显示图片所有的exif信息
    # print("showing res of getExif: \n")
    # print(tags)
    # print("\n\n\n\n");
    if FIELD in tags:
        print("\nstr(tags[FIELD]): %s" % (str(tags[FIELD])))  # 获取到的结果格式类似为：2018:12:07 03:10:34
        print("\nstr(tags[FIELD]).replace(':', '').replace(' ', '_'): %s" % (
            str(tags[FIELD]).replace(':', '').replace(' ', '_')))  # 获取结果格式类似为：20181207_031034
        print("\nos.path.splitext(filename)[1]: %s" % (os.path.splitext(filename)[1]))  # 获取了图片的格式，结果类似为：.jpg
        new_name = str(tags[FIELD]).replace(':', '').replace(' ', '_') + os.path.splitext(filename)[1]
        print("\nnew_name: %s" % (new_name))  # 20181207_031034.jpg

        time = new_name.split(".")[0][:13]
        new_name2 = new_name.split(".")[0][:8] + '_' + filename
        print("\nfilename: %s" % filename)
        print("\n%s的拍摄时间是: %s年%s月%s日%s时%s分" % (filename, time[0:4], time[4:6], time[6:8], time[9:11], time[11:13]))

        # 可对图片进行重命名
        # new_full_file_name = os.path.join(imgpath, new_name2)
        # print(old_full_file_name," ---> ", new_full_file_name)
        # os.rename(old_full_file_name, new_full_file_name)
    else:
        print('No {} found'.format(FIELD), ' in: ', filename)


def run():
    img_file = '/Users/baoqiang/Downloads/1.JPG'
    getExif(img_file)


if __name__ == '__main__':
    run()
