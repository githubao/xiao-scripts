#!/usr/bin/env python
# encoding: utf-8

"""
@description: 链家爬虫的数据处理

@author: pacman
@time: 2018/2/11 11:34
"""

import json

root_path = 'C:\\Users\\xiaobao\\Desktop'

faraway_communities = ['桃园公寓', '冠雅苑', '温泉花园', '北亚花园', '沙河镇南一村', '沙河一通', '沙河地质研究院家属楼', '毛条小区']
faraway_towns = ['南口', '西关环岛']


def process():
    not_print_key = True

    with open('{}/lianjia.json'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/lianjia.txt'.format(root_path), 'w', encoding='utf-8') as fw:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            json_data = json.loads(line.strip())

            structure = json_data['structure']
            if '车位' in structure or '车库' in structure:
                continue

            price = json_data['price']
            if price > 400:
                continue

            size = float(json_data['size'])
            if size < 40:
                continue

            district = json_data['district']
            if district not in ['昌平', '海淀', '朝阳']:
                continue

            fav_count = json_data['fav_count']
            if fav_count < 100:
                continue

            community = json_data['community']
            if community in faraway_communities:
                continue

            town = json_data['town']
            if town in faraway_towns:
                continue

            floor = json_data['floor']
            if '地下室' in floor:
                continue

            structure = json_data['structure']
            if '房间' in structure:
                continue

            # 粘贴到excel id显示异常的问题
            json_data['id'] = 'A{}'.format(json_data['id'])

            sort_dic = custom_sort(json_data)

            if not_print_key:
                key = '\t'.join(item[0] for item in sort_dic)
                fw.write('{}\n'.format(key))
                not_print_key = False

            value = '\t'.join('{}'.format(item[1]) for item in sort_dic)
            fw.write('{}\n'.format(value))


def custom_sort(dic):
    keys = ['id', 'title', 'price', 'size', 'fav_count',
            'district', 'town', 'street', 'subway', 'community',
            'floor', 'structure', 'direction',
            'url', 'size_inuse', 'unit']
    sorted_lst = []

    for key in keys:
        sorted_lst.append((key, dic[key]))

    return sorted_lst


def main():
    process()


if __name__ == '__main__':
    main()

"""
希望的条件：
300万以内，离地铁近而且尽量市里，2室1厅，50-70平，海淀、昌平或者朝阳。

必须的条件：
- 价格不大于400万
- 位置要海淀朝阳昌平，不要车位和燕郊
- 大小不小于40平
- 关注度不小于100
"""

"""
链家显示28329个数据，爬虫20856条记录，去除上面的四个条件，剩下570条
"""

"""
具体房源

400万以下：
霍营-华龙苑南里(霍营500m)
立水桥-合立方(立水桥500m)

300万以下：
沙河-民园小区(沙河2km)
龙泽-龙华园(龙泽1km)

暂不考虑：
沙河-北街家园(沙河高教园2.5km)
北七家-名佳花园(天通苑北2.7km)
北七家-燕城苑(天通苑北2.7km)

不要：
北七家-桃园公寓&冠雅苑(天通苑北4.3km)
北七家-温泉花园&北亚花园(天通苑北5km)
沙河-沙河镇南一村(巩华城3.1km)
沙河-沙河一通&沙河地质研究院家属楼(巩华城4.7km)
沙河-毛条小区(巩华城5.4km)

"""
