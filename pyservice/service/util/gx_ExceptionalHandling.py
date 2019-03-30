# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 08:13:36 2019

@author: Zcy
"""
import numpy as np 
import pandas as pd
#异常检测 并填充
def anomalyDetection(Data,data_min,data_max,len_min):
    data=np.array(Data)
    arr=[]
    for i in range( len(data)):
        if data[i]==0:
            data[i]=np.nan
        else:
            arr.append(data[i])
    mean_=np.mean(arr)
    if np.isnan(mean_):
        mean_=0
    if len(data)<=len_min:
        return None,mean_,False
    std_=np.std(data)
    data[data<=data_min]=np.nan
    data[data>=data_max]=np.nan
    max_=mean_+(3*std_)
    min_=mean_-(3*std_)
    data_anomaly={}       #存储异常值
    for j in range(len(data)):
        if data[j]>max_ or data[j]<min_ or data[j]==0:
            data_anomaly[j]=data[j]
            print(data_anomaly[j])
            data[j]=np.nan
    status=True
    if len(np.where(np.isnan(data))[0])==len(data):
        staus=False
    return data,mean_,status



#数据填充
def dataFilling(Data,num,enforce=False):
    data=pd.Series(Data)
    data=data.interpolate()
    if not enforce:
        data=pd.Series(Data)
        data=data.interpolate()
        data=data.fillna(method='ffill')
        data=data.fillna(method='bfill')
        data=np.array(data)
    data=np.array(Data)
    data[np.isnan(data)]=num
    return data
    
    
    