#-*- encoding:utf-8 -*-
import scrapy
from BaiduYun.items import BaiduyunItem
from scrapy import Request
import re
import json
import threading
q=threading.Lock()
import time
class BaiduyunSpider(scrapy.Spider):
    name = "Baiduyun"
    start_urls = ["http://yun.baidu.com/pcloud/friend/getfanslist?query_uk=3691288441"]
    allowed_domains = ["pan.baidu.com", "yun.baidu.com"]
    global n;
    n = 0

    def parse_share(self, response):
        global n
        #print response.url
        pattern = re.compile('window.yunData =(.*);')
        result = re.findall(pattern, response.body)
        try:
            result_json = json.loads(result[0])
        except IndexError:
            time.sleep(122)
            return
            #print response.meta['id'] + '  response;' + str(response.status)
        items = []
        try:
            if result_json['feedata']['total_count'] == 0:
                return
        except TypeError:
            return

        user_name = result_json['uinfo']['uname']
        user_ava_url = result_json['uinfo']['avatar_url']
        user_id = result_json['uinfo']['uk']
        user_url= 'https://pan.baidu.com/wap/share/home?uk=' + str(user_id)
        file_count = result_json['feedata']['total_count']
        for x in result_json['feedata']['records']:
            item = BaiduyunItem()
            item['userName'] = user_name
            item['userAvaUrl'] = user_ava_url
            item['userId'] = user_id
            item['title'] = x['title']
            try:
                item['shareId'] = x['shareid']
            except KeyError:
                continue
            item['userUrl'] = user_url
            items.append(item)

        n += 1
        if file_count / 20 + 1 > n:
            start = n * 20
            items.append(Request(url='https://pan.baidu.com/wap/share/home?uk=' + str(user_id) + '&start=' + str(start),  callback=self.parse_share))
        return items

    def parse_fans(self, response):
        fan_json = json.loads(response.body)
        try:
            fans_count = fan_json['total_count']
        except KeyError:
            time.sleep(122)
            return
        page_num = fans_count/15+1
        for crawl_page in range(1, page_num):
            for fan_detail in fan_json['fans_list']:
                yield Request(url='https://pan.baidu.com/wap/share/home?uk=' + str(fan_detail['fans_uk']), callback=self.parse_share)
                yield Request(url='http://yun.baidu.com/pcloud/friend/getfollowlist?query_uk='+str(fan_detail['fans_uk']), callback=self.parse_follow)
                #yield Request(url='http://yun.baidu.com/pcloud/friend/getfanslist?query_uk=' + str(fan_detail['fans_uk'])+'&start='+str(15*crawl_page), callback=self.parse_fans)

    def parse_follow(self, response):
        follow_json = json.loads(response.body)
        try:
            follow_count = follow_json['total_count']
        except KeyError:
            time.sleep(122)
            return
        page_num = follow_count / 15 + 1
        #for crawl_page in range(1, page_num):
        for fan_detail in follow_json['follow_list']:
            yield Request(url='https://pan.baidu.com/wap/share/home?uk=' + str(fan_detail['follow_uk']), callback=self.parse_share)
                #yield Request(url='http://yun.baidu.com/pcloud/friend/getfollowlist?query_uk=' + str(fan_detail['follow_uk'])+'&start='+str(15*crawl_page), callback=self.parse_follow, )
                #yield Request(url='http://yun.baidu.com/pcloud/friend/getfanslist?query_uk=' + str(fan_detail['follow_uk']), callback=self.parse_fans)

    def parse(self, response):
        fan_json = json.loads(response.body)
        try:
            fans_count = fan_json['total_count']
        except KeyError:
            time.sleep(122)
            return
        page_num = fans_count/15+1

        for crawl_page in range(1, page_num):
            yield Request(url='http://yun.baidu.com/pcloud/friend/getfanslist?query_uk=1949795117&start='+str(15*crawl_page), callback=self.parse)
            for fan_detail in fan_json['fans_list']:
                yield Request(url='https://pan.baidu.com/wap/share/home?uk=' + str(fan_detail['fans_uk']), callback=self.parse_share)
                yield Request(url='http://yun.baidu.com/pcloud/friend/getfollowlist?query_uk='+str(fan_detail['fans_uk']), callback=self.parse_follow)
                #yield Request(url='http://yun.baidu.com/pcloud/friend/getfanslist?query_uk=' + str(fan_detail['fans_uk']), callback=self.parse_fans)


