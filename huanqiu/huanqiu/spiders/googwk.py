#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/17 14:48
# @Author  : Qujiangtao
# File  : googwk.py
# user : Qujiangtao-PC

import scrapy
import requests
from lxml import etree

class PeopleSpider(scrapy.Spider):
    name = 'googwk'
    start_urls = ['https://www.gongwk.com/article.jhtml']
    def parse(self, response):
        #print(response.text)
        base = response.xpath('.//div[@class="col-md-3 hot-list"]')
        #print(base)
        for i in base:
            #标题
            title = i.xpath('div/a/@alt').extract()[0]
            #各项详情页网址
            urls = i.xpath('div/a/@href').extract()[0]
            #专题图片
            imgs = i.xpath('div/a/img/@src').extract()[0]
            print(title,urls,imgs)
            yield scrapy.Request(urls,self.show)
    #进入详情页
    def show(self, response):
        #print(response.text)
        for j in response.xpath('.//li[@class="list-group-item"]'):
            fenlei = j.xpath('span[1]/text()').extract()[0]
            title = j.xpath('a/text()').extract()[0]
            title_urls = j.xpath('a/@href').extract()[0]
            yuedu = ''.join(j.xpath('span[2]//text()').extract())
            times = ''.join(j.xpath('span[3]/text()').extract())
            print(fenlei,title,title_urls,'\t'+yuedu,'\t'+times)
            yield scrapy.Request(title_urls, self.show2)
    #进入标题详情页
    def show2(self, response):
        #print(response.text)
        contents = '\n'.join(response.xpath('//div[@id="article-content"]/p/text()').extract())
        print(contents)







