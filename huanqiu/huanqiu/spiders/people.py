#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 9:36
# @Author  : Qujiangtao
# @Email : Qujiangtao0213@163.com
# @Site :  
# @File : people.py 
# @Software: PyCharm

import scrapy
from ..items import PeopleItem
from scrapy.loader import ItemLoader


class PeopleSpider(scrapy.Spider):
    name = 'people'
    keyword = '%D2%BB%B4%F8%D2%BB%C2%B7'
    start_urls = [
        'http://search.people.com.cn/cnpeople/search.do?pageNum=1&keyword=' + keyword + '&siteName=news&facetFlag=true&nodeType=belongsId&nodeId=0']

    # print(start_urls)

    def parse(self, response):
        try:
            # print(response.url)
            domains = 'http://search.people.com.cn/'
            next_page = domains + response.xpath('//div[@class="show_nav_bar"]//a[contains(text(),"下一页")]/@href').get(
                '无')
            # print(next_page)
            hrefs = response.xpath('//div[@class="fr w800"]//b/a/@href').getall()
            # print(hrefs)
            for href in hrefs:
                yield scrapy.Request(href, callback=self.get_detail)
            REQUEST_HEADERS = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            }
            # 有许多重定向，要 dont_filter
            # self.get_detail(response)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True, headers=REQUEST_HEADERS, )
        except Exception as e:
            print(e)
        else:
            pass
        finally:
            pass

    def get_detail(self, response):
        # print(response.url)
        title = response.xpath('//h1/text()').get()
        # print(title)
        IL = ItemLoader(item=PeopleItem(), response=response)
        IL.add_value(field_name='title', value=title)
        return IL.load_item()