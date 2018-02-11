# -*- coding: utf-8 -*-

import scrapy
import time
from scrapy.http import FormRequest
import json

root_path = 'C:\\Users\\xiaobao\\Desktop\\'


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']

    def start_requests(self):
        requests = []

        for i in range(3):
            url = url_fmt.format(i * 20, 1518318578)
            request = FormRequest(url, callback=self.parse_item, headers=get_headers())

            requests.append(request)

        return requests

    def parse_item(self, response):
        json_data = json.loads(response.body.decode())

        house_lst = []

        print(json_data)

        for item in json_data['data']['list']:
            house = {}

            house['id'] = item['house_code']
            house['price'] = item['price']
            house['area'] = item['area']
            house['unit_price'] = item['unit_price']
            house['community_name'] = item['community_name']

            house_lst.append(house)

        with open('{}/lianjian.json'.format(root_path), 'a', encoding='utf-8') as fw:
            for item in house_lst:
                json.dump(item, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')


url_fmt = 'https://app.api.lianjia.com/house/ershoufang/searchv4?city_id=110000&has_recommend=1&limit_count=20&limit_offset={}&request_ts={}'


def get_headers():
    return {}


def get_headers1():
    headers = {
        'Cookie': 'lianjia_uuid=C328C753-8D5E-4052-8F00-86AC3118596D; lianjia_ssid=62141C3C-22B0-439A-9786-8FD8E0D520E6; lianjia_udid=2662392A-5A0E-4877-A1EC-03E69A589732; lianjia_token=2.0038a37bef42631c5b290e52deb996f70b',
        'Authorization': 'MjAxNzAzMjRfaW9zOjZmZGIyOTVjZjI3MmMyMDZjYzMxZWZiNTRkYmRiNTczNmNiMjUxYTQ=',
        'Referer': 'homepage%3Fseq%3D141%26trigger%3Dpoll',
        'Lianjia-Device-Id': '0088CCA4-BA28-403B-AEB7-F77EA55C7594',
        'User-Agent': 'HomeLink 8.3.8;iPhone8,1;iOS 9.3;',
        'Lianjia-Access-Token': '2.0038a37bef42631c5b290e52deb996f70b',
        'Lianjia-Timestamp': 1518318578.978744,
        'extension': 'app_tdid=h1a767153b8cdc9286fd88fadcaff7665&lj_idfa=2662392A-5A0E-4877-A1EC-03E69A589732&lj_idfv=3A59C33E-9417-445C-8F33-B110EB08C629&lj_device_id_ios=C328C753-8D5E-4052-8F00-86AC3118596D&lj_keychain_id=0088CCA4-BA28-403B-AEB7-F77EA55C7594',
        'Page-Schema': 'ershou%2Fhomepage',
        'Lianjia-Im-Version': '1',
        'Lianjia-Version': '8.3.8',
        'Host': 'app.api.lianjia.com'
    }

    return headers
