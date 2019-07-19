# -*- coding: utf-8 -*-
import time
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import HuanqiuItem
class AppsSpider(CrawlSpider):
    name = 'apps'
    start_urls = ['http://tech.huanqiu.com/']

    rules = {
        #取出每个分类链接
        Rule(LinkExtractor(allow=r'http://tech.huanqiu.com/\w+/'), follow=True),
        #分页链接(取前十页)
        Rule(LinkExtractor(allow=r'http://tech.huanqiu.com/\w+/{page}\.html'.format(page=[i for i in range(1,11)])), follow=True),
        #详情页链接
        Rule(LinkExtractor(allow=r'http://tech.huanqiu.com/\w+/\d{4}-\d{2}/\d{8}\.html'), callback='parse_item', follow=False)
    }

    def parse_item(self, response):
        print(response.text)
        title = response.xpath('//h1/text()').getall()
        time = response.xpath('//div[@class="la_tool"]/span/text()').getall()
        author = response.xpath('//span[@class="author"]/text()').get()
        print(title,time,author)




