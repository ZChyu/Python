# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:22:12 2018

@author: summer
"""
import pandas as pd
import numpy as np

def corr(data):
    corr_res=pd.DataFrame(data).corr()
    corr_data=corr_res.get_values()
    corr_index=list(corr_res.index)
    corr_len=len(corr_index)
    res_f=[]
    for i in range(1,corr_len):
        for j in range(i):
        	corr_v=corr_data[i,j]

        	if corr_v!=corr_v:
        		corr_v=0.0
        	
        	corr_v=np.round(abs(corr_v),4)
        	res_f.append({'s':corr_index[i],'t':corr_index[j],'v':corr_v})
    res={'code':'200','data':res_f}
    return res
