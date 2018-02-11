#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: pacman
@time: 2018/2/11 11:34
"""

root_path = 'C:\\Users\\xiaobao\\Desktop'


def process():
    with open('{}/lianjia.txt'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/result.txt'.format(root_path), 'w', encoding='utf-8') as fw:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            attrs = line.strip().split('\t')
            if len(attrs) != 12:
                # print(len(attrs), line)
                continue

            house_type = attrs[2]
            if '车位' in house_type or '车库' in house_type:
                continue

            price = float(attrs[7])
            if price > 400:
                continue

            location = attrs[10]
            if '燕郊' in location:
                continue

            house_size = attrs[3]
            house_size = float(house_size.replace('平米', ''))
            if house_size < 40:
                continue

            fw.write('{}\n'.format(line))


def main():
    process()


if __name__ == '__main__':
    main()

"""
必须的条件：
1. 300万可接受，不可能超过400万
2. 必须要在地铁附近
3. 最好两室，酌情考虑1室
4. 最好是南卧
5. 无论如何不能小于40平，70平就非常好了
6. 海淀或者朝阳的，第二选择昌平
"""


