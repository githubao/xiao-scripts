#!/usr/bin/env python
# encoding: utf-8

"""
@description: 即刻爬虫

@author: baoqiang
@time: 2018/12/18 下午12:45
"""
import json

import scrapy
from scrapy import FormRequest
import sys

from xiaoscript.config import get_root_path

out_file = '{}/jike.json'.format(get_root_path())

url_fmt = 'https://app.jike.ruguoapp.com/1.0/topics/listSimilarTopics?id={}'
web_fmt = 'https://web.okjike.com/topic/{}/official'
app_fmt = 'http://m.jike.ruguoapp.com/topics/{}'


class JikeSpider(scrapy.Spider):
    name = 'jike'
    cnt = 0
    processed_set = set()

    def start_requests(self):
        with open('../data/jike.txt') as f:
            for line in f:
                url = url_fmt.format(line.strip())
                yield FormRequest(url, callback=self.parse_cate)

    def parse_cate(self, response):
        datas = []

        jdata = json.loads(response.body_as_unicode())

        for item in jdata['data']:
            dic = {}

            dic['id'] = item['id']
            dic['topic_id'] = item['topicId']
            dic['web_url'] = web_fmt.format(item['id'])
            dic['app_url'] = app_fmt.format(item['id'])
            dic['name'] = item['content']
            dic['desc'] = item['briefIntro']
            dic['lastpost_at'] = item['lastMessagePostTime']
            dic['create_at'] = item['createdAt']
            dic['update_at'] = item['updatedAt']
            dic['count'] = item['subscribersCount']
            dic['topic_type'] = item["topicType"]
            dic['from_url'] = web_fmt.format(item['refRemark']["refTopic"])

            datas.append(dic)

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in datas:
                if item['id'] in self.processed_set:
                    continue
                else:
                    self.processed_set.add(item['id'])

                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

        if len(self.processed_set) % 1000 == 0:
            print('process cnt: {}'.format(len(self.processed_set)))
            sys.stdout.flush()

        for item in datas:
            yield FormRequest(url_fmt.format(item['id']), callback=self.parse_cate)


if __name__ == '__main__':
    pass
