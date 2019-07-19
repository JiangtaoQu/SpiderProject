#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/9 7:45
# @Author  : Qujiangtao

import scrapy
from scrapy.loader import ItemLoader
from ..items import HuanqiuItem


class FoodSpider(scrapy.Spider):
    name = 'yaopin'
    start_urls = ['http://bz.cfsa.net.cn/db']

    def start_requests(self):
        url = 'http://bz.cfsa.net.cn/db'
        form_data = {
            'task': 'listStandardGJ',
            'accessData': 'gj',
        }
        yield scrapy.FormRequest(url=url, formdata=form_data, callback=self.parse)

    def parse(self, response):
        codes = response.xpath('//a[@href="javascript:void(0)"]/@onclick').re(r"\('(.*?)',")
        for code in codes:
            url = 'http://bz.cfsa.net.cn/staticPages/{}.html'.format(code)
            # print(url)
            yield scrapy.Request(url, self.show1)

    def show1(self, response):
        yao = response.xpath('//span[@class="list_zt_top"]/i/text()').getall()
        # print(yao)
        # title = yao[0]
        # eng_title = yao[1]
        # type = yao[2]
        # date = yao[3]
        # execute_date = yao[4]
        # lable = yao[5]
        # committee = yao[6]
        IL = ItemLoader(item=HuanqiuItem(), response=response)
        IL.add_value(field_name='title', value=yao[0])
        IL.add_value(field_name='eng_title', value=yao[1])
        IL.add_value(field_name='type', value=yao[2])
        IL.add_value(field_name='date', value=yao[3])
        IL.add_value(field_name='execute_date', value=yao[4])
        IL.add_value(field_name='lable', value=yao[5])
        IL.add_value(field_name='committee', value=yao[6])
        return IL.load_item()