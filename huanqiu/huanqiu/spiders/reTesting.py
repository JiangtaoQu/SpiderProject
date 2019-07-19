#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/13 8:41
# @Author  : Qujiangtao
# @Email : Qujiangtao0213@163.com
# @Site :  
# @File : reTesting.py 
# @Software: PyCharm


# import re
# a = 'http://www.team.com/iteam?name=a'
# b = 'https://www.team.com/iteam?name=b'
# c = 'https://www.team.com/stu?name=c'
#
# l = re.compile(r'(http|https)://www.team.com/(iteam|stu)\?name=[abc]{1}').match(c)
#
# print(l)
#
# names = ['abf','bfbf','cfbfb','dfbb','efbf']
# na = [name.capitalize() for name in names]
# print(na)
#
#
#
#
from itertools import permutations
n=[]
for i in permutations('1234',3):
    n.append(''.join(i))
print(n)
print('可组成{}个三位数'.format(len(n)))
