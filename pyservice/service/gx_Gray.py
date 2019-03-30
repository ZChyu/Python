# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 17:17:52 2018

@author: summer
"""

import numpy as np
import math
import json

def model(X):
    #计算数据矩阵B和数据向量Y
    # X0：dict转为array
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
        print('a:',a,'\nu:',u)
        #建立灰色预测模型
        XX0 = np.zeros(n)
        XX0[0] = X0[0]
        for i in range(1,n):
            XX0[i] = (X0[0] - u/a)*(1-math.exp(a))*math.exp(-a*(i))
        print('拟合数据XX0:',XX0)
      #  m = 12   #请输入需要预测的年数
        f = np.zeros(m)
        for i in range(0,m):
            f[i] = (X0[0] - u/a)*(1-math.exp(a))*math.exp(-a*(i+n)) 
        data=f
    return {'code':'200','data':list(data)}

