#!/usr/bin/env python
# encoding: utf-8

"""
@description: 暖房

@author: pacman
@time: 2017/11/1 15:01
"""

import scrapy
from scrapy.http import FormRequest
import json
from xiaoscript.config import get_root_path

out_file = '{}/nuanfang.json'.format(get_root_path())
out_file2 = '{}/nuanfang.txt'.format(get_root_path())

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13E234 MicroMessenger/6.5.20 NetType/WIFI Language/zh_CN'
}


class NuanfangSpider(scrapy.Spider):
    name = 'nuanfang'

    def start_requests(self):
        for i in range(1, 1001):
            # for i in range(1, 3):
            url = url_fmt.format(i)
            yield FormRequest(url, headers=headers, callback=self.parse_cate)

    def parse_cate(self, response):
        data = response.body.decode()

        with open(out_file, 'a', encoding='utf-8') as fw:
            json.dump(json.loads(data), fw, sort_keys=True, ensure_ascii=False)
            fw.write('\n')


## 8272个2500以下的房间
url_fmt = 'https://nuan.io/get-room-results?rentType=shared&source%5B%5D=doubangroup&source%5B%5D=58&source%5B%5D=ganji&source%5B%5D=anjuke&source%5B%5D=soufang&source%5B%5D=nuan&bedroomAll=true&priceMax=2500&keyword=&city=bj&pageNo={}'


def trim(title):
    return title.replace('\n', '').replace('\t', '')


def process():
    with open(out_file, 'r', encoding='utf-8') as f, \
            open(out_file2, 'w', encoding='utf-8') as fw:
        for line in f:
            json_data = json.loads(line.strip())

            for item in json_data['rooms']:
                fw.write(
                    '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
                        .format(item['id'], trim(item['title']), item['url'], item.get('floor', 0),
                                item.get('price', 0), item.get('district', 0), item.get('zone', 0),
                                item.get('roomType', 0), item['postTime'], item.get('size',''), item['source']))


def get_(dic, key):
    return {}.get(key, 0)


def main():
    process()


if __name__ == '__main__':
    main()
