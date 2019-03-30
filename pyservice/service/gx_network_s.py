# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:32:53 2019

@author: Zcy
"""
import gx_network
def getNetworkSingle(Data):
    n=Data['n']
    mode=Data['mode']
    data=Data['data']
    T=Data['T']
    D=Data['D']+1
    t=0
    data_y=[]
    data_x=[]
    while (t+T)<len(data):  
        x=[]
        for i in range(t,t+T):
            x.append(data[i])
        data_y.append(data[t+T])
        data_x.append(x)
        t=t+D
    Data['x_data']=data_x
    Data['y_data']=data_y



    
    if mode=='predict':
        j=1
        datax=[]
        for i in range(n):
            datax.append(data_x[len(data_x)-j])
            j=j+1
        Data['x_data']=datax[::-1]
        res=gx_network.getJson(Data)
    elif mode=='train_one':      
        res=gx_network.getJson(Data)
    elif mode=='train_two':      
        res=gx_network.getJson(Data)
    else:
        res={"json":'please set right mode!'}
    return res

