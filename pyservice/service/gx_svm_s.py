# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 10:06:08 2019

@author: Zcy
"""
from gx_svml import gx_svmtest
import numpy as np
def getSvmSingle(Data):  
    data=Data['data']
    T=Data['T']
    n=Data['n']
    D=Data['D']+1
    t=0
    data_x=[]
    while (t+T)<len(data):  
        x=[]
        for i in range(t,t+T):
            x.append(data[i])
        x.append(data[t+T])
        data_x.append(x)
        t=t+D
    Data['train_data']=data_x
    Data['mode']='train'   
    resTrain=gx_svmtest.trainANDpredict(Data)
    #预测
    j=1
    datax=[]
    for i in range(n):
        datax.append(data_x[len(data_x)-j])
        j=j+1
    data_new=datax[::-1]
    data_new=np.array(data_new)
    Data['pridict_data']=data_new[:,0:len(data_new[0])-1]
    print(Data['pridict_data'])
    Data['mode']='predict'
    res=gx_svmtest.trainANDpredict(Data)

    
    return res