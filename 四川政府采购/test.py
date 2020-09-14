#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：ProjectTendering -> sichuangov
@IDE    ：PyCharm
@Author ：Mr. Qu
@Date   ：2020/9/4 17:41
@Desc   ：
=================================================='''
from CurrentProject.proxy2 import proxy_ip
from CurrentProject.user_agent import random_ua
from retrying import retry
import requests
import time
from lxml import etree
import re
import calendar
from pyquery import PyQuery as pq
from CurrentProject import my_sql
from CurrentProject import my_sql2


class sichuangov(object):
    def __init__(self):
        """
        初始化请求参数
        :param url
        :param header
        """
        # 目标网址
        self.url = 'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?'
        # 请求头
        self.header = {
            'Host': 'www.ccgp-sichuan.gov.cn',
            'User-Agent': str(random_ua()).replace('{', '').replace('}', ''),
        }
        # url携带参数
        today = time.strftime("%Y-%m-%d")
        page_num = 1
        self.parmes = {
            'method': 'search',
            'years': '2018',
            'chnlNames': '\u6240\u6709',  # unicode解码。结果为所有
            'chnlCodes': '',  # nom
            'title': '',
            'tenderno': '',
            'agentname': '',
            'buyername': '',
            'startTime': today,
            'endTime': today,
            'distin_like': '510000',
            'city': '',
            'town': '',
            'cityText': '\u8BF7\u9009\u62E9',
            'townText': '\u8BF7\u9009\u62E9',
            'searchKey': '',
            'distin': '',
            'type': '',
            'beginDate': '',
            'endDate': '',
            'str1': '',
            'str2': '',
            'pageSize': '10',
            'curPage': page_num,
            'searchResultForm': 'search_result_anhui.ftl'
        }

    def __str__(self):
        """
        格式化输出参数
        :return:
        """
        return self.header, self.parmes, self.url

    # 在停止之前尝试的最大次数，最后一次如果还是有异常则会抛出异常，停止运行，默认为5次
    @retry(stop_max_attempt_number=5)
    # 获取当前页面源码
    def get_source(self, parmes):
        """
        根据传递的参数获取源码
        :param parmes: 因为parmes不同的类型页数不同
        :return: 页面源码
        """
        # 代理ip
        proxies = proxy_ip()
        # 请求网页
        response = requests.get(url=self.url, params=parmes, proxies=proxies, timeout=(3, 7))
        if response.status_code == 200:
            source = response.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
            # print('11111111111111',source)
            # 获取当前最大页数
            current_max_page = re.findall('span">页次:1/(.*?)\s</div>', source, re.S)
            return source, current_max_page

    # 列表的url
    def get_page(self, parmes):
        """
        :param parmes:
        :return:
        """
        source = self.get_source(parmes)[0]
        html = etree.HTML(source)  # 通过etree.Html  解析网页结构
        list_url = html.xpath('//div[@class="info"]/ul/li/a/@href')
        # global uls  # 全局urls
        for i in list_url:
            # 拼接url
            if 'http://202.61.88.152:9002/' in i:
                print(i)
            else:
                urls = 'http://www.ccgp-sichuan.gov.cn' + ''.join(i)  # url
                # print('2222222222',urls)
            detail = requests.get(urls)
            # print(detail)
            if detail.status_code == 200:
                detail = detail.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
                # print(detail)
                html = etree.HTML(detail)  # 通过etree.Html  解析网页结构
                titles = html.xpath('/html//div[2]/div[2]/h1/text()')  # 标题
                types = html.xpath('//*[@class="siteBox"]/a[3]/text()')
                types = ''.join(types).strip()  # 类型
                # 时间转时间戳
                times = html.xpath('/html//div[2]/div[2]/p/text()')
                times = ''.join(re.findall('(\d{4}.\d{2}.\d{2}\s\d{2}.\d{2})', str(times), re.S))
                time_array = time.strptime(times, "%Y-%m-%d %H:%M")
                # 结构化时间转时间戳
                times = int(time.mktime(time_array))  # 时间
                # 内容
                doc = pq(detail)  # 初始化为PyQuery对象
                # con = doc('[class="table"]').html().replace("&#13;", "").strip().encode("gbk", 'ignore').decode("gbk", "ignore")
                con = doc('[class="table"]').html()
                global contents
                if con == None:
                    pass
                else:
                    # print(type(con))
                    contents = re.sub('style=".*?"|<!--[\s\S]*?-->|<script[\s\S]*?<\/script>', '', con)
                    contents = str(contents).replace("&#13;", "").strip().encode("gbk", 'ignore').decode("gbk",
                                                                                                         "ignore")
                    contents = contents.strip().replace(' ', '').replace('\n', '')
                    # print(contents)
                # pdf
                pdfinfos = html.xpath('//*[@id="myPrintArea"]/table//tr/td[2]/a/@href')
                if len(pdfinfos) != 0:
                    pdfinfos = 'http://www.ccgp-sichuan.gov.cn/' + ''.join(pdfinfos)
                else:
                    None
                add_time = calendar.timegm(time.gmtime())  # 插入时间
                print(titles, urls, types, times, contents, pdfinfos, add_time)
                #return titles, urls, types, times, contents, pdfinfos, add_time
                """
                    存到mysql 数据库
                    类型type
                # """
                # types = "4"
                # try:
                #     '''
                #     使用replace into关键字：
                #     replace into 是insert into的增强版。在向表中插入数据时，首先判断数据是否存在；如果不存在，则插入；如果存在，则更新。即旧记录与新记录有相同的值，则在新记录被插入之前，旧记录被删除。
                #     '''
                #     sql = 'insert ignore into project_info(title,url,content,pdf,type,time,addtime)VALUES(%s,%s,%s,%s,%s,%s,%s)'
                #     my_sql.cursor.execute(sql, (titles, urls, contents, pdfinfos, types, times, add_time))
                #     my_sql.db.commit()
                #     print("写入成功")
                # except Exception as e:
                #     print("跳过")
                #     my_sql.db.rollback()  # 失败回滚
                # else:
                #     exit()
                # my_sql.cursor.close()
                # my_sql.db.close()

    # 执行函数
    def run(self):
        max_page = self.get_source(self.parmes)[1]
        max_page = ''.join(max_page)
        # print('当前最大页数:', max_page)
        for i in range(1, int(max_page) + 1, 1):
            time.sleep(2)
            print('正在爬取第{}页'.format(str(i)))
            sichuangov.parmes['curPage'] = i
            data = self.get_source(parmes=self.parmes)
            #print('这是data',data)
            #page_data = self.get_page(parmes=self.parmes)
            ll = sichuangov.get_page(parmes=self.parmes)
            #print('这是page_data',page_data)



if __name__ == '__main__':
    # 实例化
    sichuangov = sichuangov()
    sichuangov.run()




#
# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# '''=================================================
# @Project -> File   ：ProjectTendering -> sichuangov
# @IDE    ：PyCharm
# @Author ：Mr. Qu
# @Date   ：2020/9/4 17:41
# @Desc   ：
# =================================================='''
# from CurrentProject.proxy2 import proxy_ip
# from CurrentProject.user_agent import random_ua
# from retrying import retry
# import requests
# import time
# from lxml import etree
#
#
# class sichuangov(object):
#     def __init__(self):
#         """
#         初始化请求参数
#         :param url
#         :param header
#         """
#         # 目标网址
#         self.url = 'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?'
#         # 请求头
#         self.header = {
#             'Host': 'www.ccgp-sichuan.gov.cn',
#             'User-Agent': str(random_ua()).replace('{', '').replace('}', ''),
#         }
#         # url携带参数
#         self.parmes = {
#             'method': 'recommendBulletinList',
#             'rp': '25',
#             'page': '1',  # 当前页数
#             'moreType': 'provincebuyBulletinMore',  # 省级
#             'channelCode': 'sjcg1'  # 省级采购1
#         }
#     def __str__(self):
#         """
#         格式化输出参数
#         :return:
#         """
#         return self.header, self.parmes, self.url
#
#     # 在停止之前尝试的最大次数，最后一次如果还是有异常则会抛出异常，停止运行，默认为5次
#     @retry(stop_max_attempt_number=5)
#     def get_source(self, parmes):
#         """
#         根据传递的参数获取源码
#         :param parmes: 因为parmes不同的类型页数不同
#         :return: 页面源码
#         """
#         # 代理ip
#         proxies = proxy_ip()
#         # 请求网页
#         response = requests.get(url=self.url, params=parmes, proxies=proxies, timeout=(3, 7))
#         if response.status_code == 200:
#             source = response.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
#             #print(source)
#             return source
#     def  get_page(self,parmes):
#         """
#         :param parmes:
#         :return:
#         """
#         source = self.get_source(parmes)
#         html = etree.HTML(source)  # 通过etree.Html  解析网页结构
#         list_url = html.xpath('//div[@class="info"]/ul')
#         #循环遍历拿出当前页面的所有url
#         for i in list_url:
#             url = i.xpath('li/a/@href')
#             print(url)
#
#
#
#
#
#
#
#
#
#     # 执行函数
#     def run(self):
#         # data = self.get_source(url=self.url, header=self.header, parmes=self.parmes)
#         #data = self.get_source(parmes=self.parmes)
#         data = self.get_source(parmes=self.parmes)
#         page_data = self.get_page(parmes=self.parmes)
#
#
# if __name__ == '__main__':
#     # 实例化
#     sichuangov = sichuangov()
#     sichuangov.run()
