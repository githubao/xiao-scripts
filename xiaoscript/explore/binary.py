#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: baoqiang
@time: 2019/10/24 12:47 下午
"""
import binascii

s = '01000001 01101100 01110111 01100001 01111001 01110011 00100000 01000100 01100001 01111001 00100000 00110001 111001011010011110001011 111001111011101110001000 111001011000001110001111 111001011000100010011011 111001001011100010011010 111001111010110010101100 111001001011100010000000 111001011010010010101001 111010011000001010100011 111001101010000010110111 111001101000100110111110 00100000 01100010 01110101 01100111'


def run():
    res = []

    items = s.split(' ')
    for item in items:
        if len(item) == 24:
            for i in range(3):
                a = hex(int(item[8 * i:8 * (i + 1)], 2))
                a = a.replace('0x', '\\x')
                res.append(a)
        else:
            a = hex(int(item, 2))
            a = a.replace('0x', '\\x')
            res.append(a)

    aaa = ''.join(res)

    b2 = binascii.a2b_hex(aaa.replace('\\x', ''))
    print(b2.decode('utf-8'))


if __name__ == '__main__':
    run()
