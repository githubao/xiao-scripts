#!/usr/bin/env python
# encoding: utf-8

"""
@description: 京东书籍

@author: baoqiang
@time: 2019-06-26 13:00
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from xiaoscript import config
from threading import Lock
import json
import requests
import re

# 图书 小说
start_url = 'https://list.jd.com/list.html?cat=1713,3258&page=1&delivery=1&sort=sort_rank_asc'
comment_url_fmt = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'

id_pat = re.compile('https://item.jd.com/([\\d]+).html')

out_file = '{}/jd_book.json'.format(config.get_root_path())


# https://club.jd.com/comment/productCommentSummaries.action?referenceIds=12178407
# 先爬取id,后续批量协程更新评论
class JdBookSpider(CrawlSpider):
    name = 'jdbook_spider'
    start_urls = [start_url, ]

    links1 = LinkExtractor(allow='.*cat=\\d+,\\d+$')
    links2 = LinkExtractor(allow='.*cat=\\d+,\\d+,\\d+$')
    links3 = LinkExtractor(allow='.*cat=\\d+,\\d+,\\d+&page=[\\d]&sort=sort_rank_asc.*')

    rules = (
        Rule(links1, follow=True),
        Rule(links2, follow=True),
        Rule(links3, callback='parse_cate', follow=True)
    )

    lock = Lock()

    def parse_cate(self, response):
        # get cate
        cate_url = response.selector.xpath('.//div[@class="crumbs-nav"]//span[@class="curr"]/text()')
        cate1 = '图书'
        cate2 = cate_url[0].extract().strip()
        cate3 = cate_url[1].extract().strip()

        classes = response.selector.xpath('.//div[@id="plist"]//li[@class="gl-item"]')

        datas = []

        for item in classes:
            dic = {'from_url': response.url, 'cate': '{}/{}/{}'.format(cate1, cate2, cate3)}

            # price_url = item.xpath('.//div[@class="p-price"]//i/text()')
            # dic['price'] = float(price_url[0].extract().strip())

            name_url = item.xpath('.//div[@class="p-name"]/a')
            txt_url = name_url.xpath('.//text()')
            dic['name'] = ''.join(i.extract().strip() for i in txt_url)

            # comment_url = item.xpath('.//div[@class="p-comment"]//a/text()')
            # dic['comment'] = trim_comment(comment_url[0].extract().strip())

            dic['url'] = 'https:{}'.format(name_url.xpath('./@href')[0].extract().strip())

            m = id_pat.match(dic['url'])
            if m:
                dic['id'] = m.group(1)
            else:
                dic['id'] = 0

            # add one
            datas.append(dic)

        # request comment
        self.request_comment(datas)

        self.write_file(datas)

    @staticmethod
    def request_comment(results):
        ids = [item['id'] for item in results]

        comment_url = comment_url_fmt.format(','.join(ids))

        resp = requests.get(comment_url)

        for idx, item in enumerate(resp.json()['CommentsCount']):
            results[idx]['cnt'] = item['CommentCount']

    def write_file(self, results):
        self.lock.acquire()

        with open(out_file, 'a', encoding='utf-8') as fw:
            for item in results:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

        self.lock.release()


def trim_comment(comment_str):
    cnt_str = comment_str.strip().replace('+', '')
    if '万' in cnt_str:
        cnt_str = cnt_str.strip('万')
        return int(cnt_str) * 1000
    else:
        return int(cnt_str)


if __name__ == '__main__':
    pass
