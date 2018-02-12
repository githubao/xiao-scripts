#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: pacman
@time: 2018/2/11 11:34
"""

import json

root_path = 'C:\\Users\\xiaobao\\Desktop'


def patch_dic(json_data):
    areas = json_data['areas']

    if len(areas) != 2 and len(areas) != 3:
        print('err: {}'.format(json_data))

    areas_str = '\t'.join(areas)
    if len(areas) == 2:
        areas_str += '\t '

    json_data['areas'] = areas_str
    del json_data['district']


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
            if district not in ['昌平', '海淀']:
                continue

            # 保证打印的area的格式
            patch_dic(json_data)

            sort_dic = sorted(json_data.items())

            if not_print_key:
                str = '\t'.join(item[0] for item in sort_dic)
                fw.write('{}\n'.format(str))
                not_print_key = False

            str = '\t'.join('{}'.format(item[1]) for item in sort_dic)
            fw.write('{}\n'.format(str))


def main():
    process()


if __name__ == '__main__':
    main()

"""
链家显示28329个数据，爬虫20195条记录，19461条有效数据，去除价格&车位&燕郊&大小，剩下5924条
海淀朝阳昌平一共有1673条
"""

"""
300万以内，离地铁近，2室1厅，50-70平，海淀或者昌平。
"""

"""
必须的条件：
1. 300万可接受，不可能超过400万
2. 必须要在地铁附近
3. 最好两室，酌情考虑1室
4. 最好是南卧
5. 无论如何不能小于40平，70平就非常好了
6. 海淀或者朝阳的，第二选择昌平


300万以下：
可选：
沙河-民园小区(沙河2km)
龙泽-龙华园(龙泽1km)
回龙观-龙城花园(生命科学园1km)

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
