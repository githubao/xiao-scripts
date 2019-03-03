#!/usr/bin/env python
# encoding: utf-8

"""
@description: 调整图片亮度

@author: baoqiang
@time: 2019/2/28 下午5:17
"""

from PIL import Image, ImageEnhance, ImageStat


def brighten(input_name, output_file, factor):
    """
    调整图片亮度到factor倍，保存结果到output_file
    """

    im = Image.open(input_name)
    enhancer = ImageEnhance.Brightness(im)
    enhanced_im = enhancer.enhance(factor)
    enhanced_im.save(output_file)


def brightness(im_file):
    image = Image.open(im_file)
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    res = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        res += ratio * (-scale + index)

    return 1 if res == 255 else res / scale


def run():
    input_file = "/Users/baoqiang/Downloads/1.jpeg"
    output_file = "/Users/baoqiang/Downloads/1.enhance.jpeg"
    factor = 1.2
    # factor = 0.2

    im_brightness = brightness(input_file)
    brighten(input_file, output_file, factor)

    print('file {} brightness is {:.6f}\nchange brightness with factor {} saved in {}'
          .format(input_file, im_brightness, factor, output_file))

    print('output brightness is {:.6f}'.format(brightness(output_file)))


if __name__ == '__main__':
    run()
