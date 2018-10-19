#!/usr/bin/env python
# encoding: utf-8

"""
@description: 嗨住租房

@author: baoqiang
@time: 2018/9/28 下午2:17
"""

import requests
import binascii
from xiaoscript import config
import json
import sys
from collections import defaultdict

url = 'https://api.loulifang.com.cn/v12/house/list.html'

req_body = {"search_id": "", "limit": 20, "money_min": 2500, "pageno": 1, "money_max": 3500, "sort": -1,
            "other_ids": [10], "stand_ids": [287], "latitude": 0, "key_self": 0, "region_ids": [], "logicSort": "0",
            "plate_ids": [], "longitude": 0, "distance": "0", "update_time": 0, "ab_test": "A", "line_ids": [],
            "type_no": 0, "key": ""}

out_file = '{}/hizhu.json'.format(config.get_root_path())


def run():
    # for i in range(1, 30):
    for i in range(1, 20):
        req_body.update({'pageno': i})
        resp = requests.post(url, json=req_body, verify=False, headers=headers)

        print(resp.status_code)

        resp_data = format_data(resp.json())
        # print(resp_data)

        with open(out_file, 'a', encoding='utf-8') as fw:
            json.dump(resp_data, fw, ensure_ascii=False)
            fw.write('\n')

        print('process cnt: {}'.format(i))
        sys.stdout.flush()


headers = {
    'Md5': '207380cc2b6fd102691ef04ad2f005fc',
    # 'User-Agent': 'Loulifang/5.4.1 (iPhone; iOS 9.3; Scale/2.00)',
    'Udid': '5D0E3A59-4C3D-4A0C-BFC8-934E2349B7D7',
    # 'Session': '3f2fadc5-e602-8003-5928-3ad09a84ae7c',
    # 'Host': 'api.loulifang.com.cn',
    # 'Time': '1538114793.193886',
    'Platform': 'iPhone',
    'CityCode': '001001',
    # 'Cookie': 'PHPSESSID=2r5emsbuba8t8fl63nf8mu1100',
    'ClientVer': '5.4.1',
    # 'OSVer': '9.3',
    # 'Accept': '*/*',
    # 'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    # 'ScreenSize': '375x667'
}


def format_data(jdata):
    s = jdata['message']
    b = bytes(ord(i) for i in s)
    jdata['message'] = b.decode('utf-8')
    return jdata


def tmp():
    b = b'\xe4\xbd\xa0\xe6\xb2\xa1\xe6\x9c\x89\xe6\x9d\x83\xe9\x99\x90\xe8\xae\xbf\xe9\x97\xae\xe6\xad\xa4\xe6\x8e\xa5\xe5\x8f\xa3'
    print(b.decode('utf-8'))

    s1 = '\xe4\xbd\xa0\xe6\xb2\xa1'
    b1 = bytes(ord(i) for i in s1)
    print(b1.decode('utf-8'))

    s2 = '\\xe4\\xbd\\xa0\\xe6\\xb2\\xa1'
    b2 = binascii.a2b_hex(s2.replace('\\x', ''))
    print(b2.decode('utf-8'))


def process_data():
    dic = defaultdict(int)

    with open(out_file, 'r', encoding='utf-8') as f:
        for line in f:
            if len(line) < 3:
                break

            jdata = json.loads(line.strip())

            for item in jdata['data']['house_list']:
                estate_name = item['estate_name']

                dic[estate_name] += 1

    ordered = sorted(dic.items(), key=lambda x: x[1], reverse=True)

    for k, v in ordered:
        print('{}: {}'.format(k, v))


if __name__ == '__main__':
    # run()
    # tmp()
    process_data()
