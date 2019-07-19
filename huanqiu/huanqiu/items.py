# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuanqiuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    eng_title = scrapy.Field()
    type = scrapy.Field()
    date = scrapy.Field()
    execute_date = scrapy.Field()
    lable = scrapy.Field()
    committee = scrapy.Field()
    hq_title = scrapy.Field()
    hq_publish_date = scrapy.Field()
    hq_author = scrapy.Field()
    hq_content = scrapy.Field()
    hq_image_url = scrapy.Field()
    hq_category = scrapy.Field()
    hq_language = scrapy.Field()
    hq_module = scrapy.Field()
    hq_html_content = scrapy.Field()
    hq_copyright = scrapy.Field()
    hq_site_name = scrapy.Field()
    hq_meta_data = scrapy.Field()
    hq_hash_code = scrapy.Field()
    hq_url = scrapy.Field()

class OfweekItem(scrapy.Item):
    title = scrapy.Field()

class PeopleItem(scrapy.Item):
    title = scrapy.Field()