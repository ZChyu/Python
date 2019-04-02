# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:30:56 2019

@author: Zcy
"""
import urllib.request as requ
import threading
import pymysql
import sifany_util
import time
import json

user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
def getUrl(url):    
    headers = { 'User-Agent' : user_agent }
    req = requ.Request(url,headers= headers)
    response = requ.urlopen(req)
    the_page = response.read()
    return the_page.decode("utf8")
'''
#获取全国所有城市代码
URL='http://www.nmc.cn/f/rest/province'
html=getUrl(URL)
provinceCode=json.loads(html)   
province=[]
for i in range(len(provinceCode)):
    province.append(provinceCode[i]['code'])
city=[]
file=open('cityCodes.txt','w')
for pcode in province:
    url=str('http://www.nmc.cn/f/rest/province/'+str(pcode))
    html=getUrl(url)
    citycode=json.loads(html)
    cicode=[]
    for i in range(len(citycode)):
        cicode.append(citycode[i]['code'])
    file.write(str(cicode))
print('success')
file.close()
'''
'''
#获取山东省城市代码
url='http://www.nmc.cn/f/rest/province/ASD'
html=getUrl(url)
citycode=json.loads(html)
cicode=[]
for i in range(len(citycode)):
    cicode.append(citycode[i]['code'])
print(cicode[0])
'''  
f=open('cityCodes.txt','r')
codess=f.read()
print((codess))
    