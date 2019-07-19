# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2019/7/10 21:03
# # @Author  : Qujiangtao
# import PyPDF2
from selenium import webdriver
import requests
from lxml import etree

driver = webdriver.Chrome()
driver.get('http://search.people.com.cn/cnpeople/news/noNewsResult.jsp')
driver.maximize_window()
driver.find_element_by_xpath('//*[@id="keyword"]').send_keys('一带一路')
driver.find_element_by_xpath('/html//div[1]/form/div[2]/table/tbody/tr/td[2]/img').click()
source = driver.page_source
#print(source)
source2 = etree.HTML(source).xpath('//div[@class="fr w800"]/ul')
for i in source2:
    title = i.xpath('li[1]/b/a/text()')
    url = i.xpath('li[1]/b/a/@href')
    print(title,url)




