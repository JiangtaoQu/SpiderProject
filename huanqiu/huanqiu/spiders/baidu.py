#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 21:20
# @Author  : Qujiangtao

import scrapy
from ..items import PeopleItem
from scrapy.loader import ItemLoader


class BaiduNewsSpider(scrapy.Spider):
    name = 'baidunews'
    # allowed_domains = ['www.test.com']
    keyword = '%E6%97%A0%E4%BA%BA%E6%9C%BA'
    start_urls = [
        'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=' + keyword + '&x_bfe_rqs=03E80&x_bfe_tjscore=0.016743&tngroupname=organic_news&pn=0']
    # print(start_urls)

    def parse(self, response):
        try:
            domains = 'https://www.baidu.com/s?'
            next_page = domains + response.xpath('//p[@id="page"]//a[contains(text(),"下一页")]/@href').get('无')
            hrefs = response.xpath('//h3[@class="c-title"]/a/@href').getall()
            h3 = response.xpath('//h3[@class="c-title"]')
            for i, j in zip(hrefs, h3):
                print(i, j.xpath('string(.//a)').get().strip(), sep='\n')
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True, )
        except Exception as e:
            print(e)