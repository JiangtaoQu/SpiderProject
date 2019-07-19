# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class HuanqiuPipeline(object):


    def process_item(self, item, spider):
        if spider.name == 'ofweek_pro':
            db_yao = pymongo.MongoClient()['huanqiu'][spider.name]
            db_yao.insert_many()
        db_yao.insert_one(dict(item))
        return item


from .spiders import baidu