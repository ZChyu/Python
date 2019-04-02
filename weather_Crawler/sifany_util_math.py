# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 14:36:29 2018

@author: lidh
"""

#import pandas as pd
from jieba import analyse
import math
import re
#def corr(x,y):
    #return pd.Series(x).corr(pd.Series(y))
def find_phone(str0):
    temp=re.findall('\D\d{11}\D',str0)
    if len(temp)==0:
        return ''
    temp=re.findall('\d{11}',temp[0])[0]
    return temp
def fetch_words(param):
    return analyse.extract_tags(param)
def trans_group(types,num):
    trans_flag=False
    if len(types)%num!=0:
        num=num-1
        trans_flag=True
    group_num=math.floor(len(types)/num)
    ran=list(range(0,len(types)+1,group_num))
    groups=[]
    for i in range(len(ran)-1):
        groups.append(types[ran[i]:ran[i+1]])
    if trans_flag and (ran[-1]!=len(types)):
        groups.append(types[ran[-1]:len(types)])
    return groups
def sort(a,field,is_desc=False):
    a.sort(key=lambda x:x[field],reverse=is_desc)
    return a
def get_num_from_str(str0):
    return re.findall('[\d.]*',str0)[0]
def get_hanzi_from_str(str0):
    return re.sub("[A-Za-z0-9\!\%\[\]\,\。\.\ ]", "", str0)
def trans_price_weight(str0):
    num=get_num_from_str(str0)
    
    if num=='':
        return -1
    unit=re.findall('\/.*',str0)[0][1:]
    if unit=='公斤':
        return num
    if unit=='斤':
        return float(num)*2
        
    if unit=='吨':
        return float(num)/1000

    return num
def trans_danwei_weight(str0):
    num=get_num_from_str(str0)
    
    if num=='':
        
        return {'num':-1,'unit':''}
    unit=get_hanzi_from_str(str0)
    if unit=='公斤':
        return {'num':float(num),'unit':'公斤'}
    if unit=='斤':
        return {'num':float(num)/2,'unit':'公斤'}
        
    if unit=='吨':
        return {'num':float(num)*1000,'unit':'公斤'}
    
    return {'num':float(num),'unit':unit}
    