#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 11:42
# @Author  : Qujiangtao
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from huanqiu.items import OfweekItem
import re
class AppsSpider(CrawlSpider):
    #handle_httpstatus_list = [403]
    name = 'ofweek_pro'
    start_urls = ['https://www.ofweek.com/']

    rules = {
        #默认（follow=False）
        Rule(LinkExtractor(allow=(r'//[\w]+\.ofweek\.com/[\w]*/*',),restrict_xpaths=('//link',)),follow=True),
        Rule(LinkExtractor(allow=(r'https://[\w]+\.ofweek\.com/[\w]*/*[\d]{4}-[\d]{2}/ART-[\d]{6}-[\d]{4}-[\d]{8}\.html',)), callback='parse_item', follow=False),
    }
    # def parse(self, response):


    def parse_item(self, response):

        #print(response.text)
        title = response.xpath('//p[@class="title"]/text()').get()
        #times = response.xpath('//div[@class="time fl"]/text()').get()
        print(title)
        ok =ItemLoader(item=OfweekItem(),response=response)
        ok.add_value(field_name='title',value=title)
        #ok.add_value(field_name='times', value=times)
        return ok.load_item()





































# import requests
# kk = requests.get('https://www.ofweek.com/').content.decode('gbk')
# print(kk)