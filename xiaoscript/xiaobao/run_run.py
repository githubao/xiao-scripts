#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

from pprint import pprint

"""
@description: python 语法测试

@author: baoqiang
@time: 2018/7/31 上午11:26
"""
import hashlib
import json

import requests
import time
import uuid
import datetime
import os
import re
from collections import OrderedDict


def run():
    # test_datetime()
    # test_json_2()
    # test_flag_and()
    # test_unique()
    # test_except()
    # test_http()
    # test_none()
    # test_date()
    # test_cls_var()
    # test_tuple_fmt()
    # test_list_unpack()
    # test_helloabc()
    # test_mkdir()
    # test_uuid()
    # test_beauty_print()
    # test_httpbin()
    # run_recom()
    # run_recom()
    test_days()

def test_httpbin():
    url = 'http://httpbin.org/post'

    data = {"age": 18}

    resp = requests.post(url, data=data)

    pprint(resp.json())


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def fill_text_to_print_width(text, width):
    stext = str(text)
    utext = stext.decode("utf-8")
    cn_count = 0
    for u in utext:
        if is_chinese(u):
            cn_count += 1
    return stext + (" " * (width - cn_count - len(utext)))


def beauty_format(title_config_pairs):
    fmt = "|".join((["{}"] * len(title_config_pairs)))
    return fmt.format(*map(lambda x: fill_text_to_print_width(x[0], x[1]), title_config_pairs))


def test_beauty_print():
    datas = [
        ['你好呀', 10],
        ['我不知道4我要干嘛', 20]
    ]
    # for i in range(1,8):
    #     items = []
    #     for j in range(1,8):
    #         items.append('*' * (i * j))
    #
    #     datas.append(items)

    msg = beauty_format(datas)
    print(msg)


# def beauty_format(matrix):
#     s = [['{}'.format(e) for e in row] for row in matrix]
#
#     s2 = [['{}'.format(e).decode('utf-8') for e in row] for row in matrix]
#     lens = [max(map(len, col)) for col in zip(*s2)]
#
#     fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
#     table = [fmt.format(*row) for row in s]
#     return '\n'.join(table)


def test_mkdir():
    path = '/Users/baoqiang/Downloads/a/b/c.txt'

    mkpath(path)


def mkpath(filename):
    if os.path.exists(filename):
        return
    path, name = os.path.split(filename)
    if os.path.exists(path):
        return
    os.makedirs(path)


def test_helloabc():
    item_id = 1234
    print('{}'.format(item_id)[0])


def test_list_unpack():
    a = [1, 2, 3]
    many_args(a)
    many_args(*a)

    # many_args2(a)
    many_args2(*a)

    many_args(4, 5, 6)
    many_args2(4, 5, 6)


def many_args(*args):
    for i in args:
        print(i)
    print('---sep---')


def many_args2(a, b, c):
    for i in [a, b, c]:
        print(i)


def test_tuple_fmt():
    # name = (1, 2, 3)
    name = [1, 2, 3]
    # name = 2

    # print('hi, %s' % (name,))
    print('hi, %s' % name)
    print('hi, {}'.format(name))


def test_cls_var():
    p1 = Person()
    p2 = Person()
    # p1.name.append(1)
    p1.name = [1]
    print(p1.name)
    print(p2.name)
    print(Person.name)


class Person:
    name = []
    # pass


def test_except():
    a = 1
    b = a / 0


def test_date():
    for i in range(1, 6):
        day = datetime.datetime.today() - datetime.timedelta(days=i)
        print(day)


def test_none():
    extra_unpacked = {'i18n_article_revenue_permission': 4}
    # extra_unpacked = {}

    article_permission = extra_unpacked.get('i18n_article_revenue_permission', None)

    if article_permission is not None and article_permission != 1:
        print(False)
    else:
        print(True)


def test_days():
    for i in range(1, 5)[::-1]:
        d = datetime.datetime.today() - datetime.timedelta(days=i)
        s = d.strftime('%Y%m%d')
        key = 'reports_status_v2:{}'.format(s)
        print(key)

    now = datetime.datetime.now()
    for d in range(now.day - 1, 0, -1):
        path = datetime.datetime(now.year, now.month, d).strftime('%Y%m%d')
        print(path)


def test_unique():
    file_path = '/Users/baoqiang/'

    with open('{}/id_old.txt'.format(file_path), 'r') as f:
        dic = {line.strip(): '' for line in f}

    with open('{}/id_new.txt'.format(file_path), 'r') as f, \
            open('{}/media_id.txt'.format(file_path), 'w') as fw:
        for line in f:
            item = line.strip()
            if item not in dic:
                fw.write('{}\n'.format(item))


def test_flag_and():
    flag = 562949953421322
    res = flag & (1 << 1)
    print(res)


def test_json():
    with open('/Users/baoqiang/Documents/tmp.json', 'r') as f, \
            open('/Users/baoqiang/Documents/tmp1.json', 'w', encoding='utf-8') as fw:
        jdata = json.loads(f.read())
        # dic = OrderedDict(jdata)
        json.dump(jdata, fw, ensure_ascii=False, sort_keys=True)


def test_json_2():
    with open('/Users/baoqiang/Documents/tmp.json', 'r') as f, \
            open('/Users/baoqiang/Documents/tmp1.json', 'w', encoding='utf-8') as fw:
        jdata = json.loads(f.read())

        dic = {}

        for key, value in jdata.items():
            if isinstance(value, list):
                dic['cnt_{}'.format(key)] = len(value)
                dic[key] = value[:3]
            else:
                dic[key] = jdata[key]

        json.dump(dic, fw, ensure_ascii=False, sort_keys=True)


def test_datetime():
    mydate = datetime.datetime.now() - datetime.timedelta(hours=1)
    hour = 5
    res = datetime.datetime.combine(mydate, datetime.time(hour))
    print(res)

    fmt = '{:02}'
    for i in range(23):
        print(fmt.format(i))


def test_http():
    headers = get_crawl_wenda_headers()

    # url = 'https://crawl.bytedance.net/crawl/contract/api/v1/contracts/get_signed_type/'
    # data = dict(uids=json.dumps([98512079999, ]))

    url = 'https://crawl.bytedance.net/crawl/contract/api/v1/contracts/get_contracts_by_id/wenda/'
    data = dict(object_ids=json.dumps([5834746111, ]))

    print(json.dumps(data))

    resp = requests.post(url, data=data, headers=headers)
    print(resp.status_code)
    print(resp.json())


def get_crawl_wenda_headers():
    import uuid
    access_key = 'TtdUh817hI'
    access_secret = 'g9!#l7zuz=8#2e3batp9*8tz#16qtnefw7hmq2ldenfx@h1fz3'
    nonce = uuid.uuid1().get_hex()
    timestamp = str(int(time.time()))
    _list = [access_secret, timestamp, nonce]
    _list.sort()
    signature = hashlib.sha1(''.join(_list)).hexdigest()
    headers = {
        'X-AccessKey': access_key,
        'X-Signature': signature,
        'X-Timestamp': timestamp,
        'X-Nonce': nonce
    }
    return headers


def test_uuid():
    u = uuid.uuid1()
    res = u.get_hex()
    print(u)
    print(res)


def test_num_mask():
    nu = '1234567890123456'
    print(mask_bank_number_last_four_bits(nu))


def mask_bank_number_last_four_bits(number):
    if not isinstance(number, basestring):
        return '-'
    if len(number) < 6:
        return '-'
    return '*' * (len(number) - 4) + number[-4:]


def test_task_day():
    # task_day = date(2018, 0o7, 12)
    # print(type(task_day))

    # task_day_str = '2134'
    # task_day = time.strptime(task_day_str, "%Y-%m-%d")
    # print(task_day)

    today = datetime.date.today()
    t = time.mktime(today.timetuple())
    print(t)


def test_third_expression():
    transfer_to_mid = 343
    s = "extra_info = '转入母账号' if transfer_to_mid > 0 else ''"
    print(s)


def test_excel_format():
    for i in range(5, 1000):
        fmt = '=IF(U5>70%,O{},IF(U5>40%,P{},Q{}))'
        print(fmt.format(i, i, i))


def test_timedelta():
    stat_day = datetime.date.today() - datetime.timedelta(days=5)
    print(stat_day)


def test_time_stamp():
    # task_day = datetime.today()

    # task_day = datetime.today() - timedelta(days=1)

    task_day = datetime.datetime(2018, 8, 2, 00, 00, 00)

    task_day_str = task_day.strftime('%Y%m%d')
    task_day_ts = int(time.mktime(task_day.timetuple()))

    print(task_day_str)
    print(task_day_ts)


if __name__ == '__main__':
    run()
