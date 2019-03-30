# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 11:54:54 2018

@author: ReedGuo
"""

import statsmodels.api as sm
import pandas as pd
import numpy as np
from util import gx_ExceptionalHandling as ExeHand
import itertools
import sys
import os

def getParams(data):
    y=data
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    param_ok=None
    param_seasonal_ok=None
    aic_ok=10000000000000
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
                results = mod.fit()
                if results.aic<aic_ok:
                    param_ok=param
                    param_seasonal_ok=param_seasonal
                    aic_ok=results.aic
            except:
                continue
    return param_ok,param_seasonal_ok,aic_ok
def predict(Data):
    data_src=np.array(Data['data'])
    data_src=data_src.astype(float)
    data_src,mean_,status=ExeHand.anomalyDetection(data_src,Data['min'],Data['max'],5)
    if not status:
        return {'pridict':list(np.ones(Data['n'])*mean_)}
    values2=ExeHand.dataFilling(data_src,mean_,True)
    values=pd.Series(ExeHand.dataFilling(data_src,mean_,True))


    
    param_ok,param_seasonal_ok,aic_ok=getParams(values.values)

    mod = sm.tsa.statespace.SARIMAX(values.values,order=param_ok,seasonal_order=param_seasonal_ok,enforce_stationarity=False,enforce_invertibility=False)
    results = mod.fit()
    pred_uc = results.get_forecast(steps=Data['n'])
    pred_ci = pred_uc.conf_int()
    resd=[]
    for i in pred_ci:
        resd.append(float((i[0]+i[1])/2))
    resd=np.array(resd)
    resds=[]
    for res in resd:
        resds.append(abs(round(res,2)))
    
    print('--------print params---------')
    print(param_ok,param_seasonal_ok)
    print(data_src)
    print(values)
    print(values2)

    print(resds)

    resds,mean__,status=ExeHand.anomalyDetection(resds,Data['min'],Data['max'],0)
    resds=ExeHand.dataFilling(resds,mean_)
    res={'pridict':list(resds)}
    return res