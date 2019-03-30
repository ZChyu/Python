# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 17:17:52 2018

@author: summer
"""
##
import numpy as np
import math
import json
import pandas as pd

def model(X):
    #计算数据矩阵B和数据向量Y
    # X0：dict转为array
    try:
        X0=X['data']
        X0=np.array(X0)
        if len(X0)==np.sum(X0==0):
            data=[]
            for i in range(int(X['n'])):
                data.append(0)
        else:
            m=  X['n']
          #  X0=np.array([[303.95], [295.24], [298.54], [297.47], [417.44], [298.68], [309.72], [309.4], [306.66], [317.01], [302.14], [300.75]])
            tmp = np.cumsum(X0)
            X1 = np.array(tmp)
            n=len(X0)
            B = np.zeros([n-1,2])
            Y = np.zeros([n-1,1])
            for i in range(0,n-1):
                B[i][0] = -0.5*(X1[i] + X1[i+1])
                B[i][1] = 1
                Y[i][0] = X0[i+1]

            #计算GM(1,1)微分方程的参数a和u
            A = np.linalg.inv(B.T.dot(B)).dot(B.T).dot(Y)
            a = A[0][0]
            u = A[1][0]
           # print('a:',a,'\nu:',u)
          #  m = 12   #请输入需要预测的年数
            f = np.zeros(m)
            for i in range(0,m):
                f[i] = (X0[0] - u/a)*(1-math.exp(a))*math.exp(-a*(i+n)) 
            data=f
            print(data)
            for da in data:
                if pd.isnull(da):
                    t=X0[np.max(np.where(X0!=0)[0])]
                    data=np.full(m,float(t))
        return {'code':'200','data':list(data)}
    except:
        print ('The data is not in the correct format')
        return {'code':'400','error':str('The data is not in the correct format')}

