# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 13:30:30 2019

@author: Zcy
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 13:26:16 2019

@author: Zcy
"""
import numpy as np
import pandas as pd
import itertools
import statsmodels.api as sm
from pandas import Series


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