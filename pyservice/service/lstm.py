# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:32:30 2018

@author: Zcy
"""

import gx_lstm as glstm
import dataProcess as dp
from keras import backend as K  # Keras解决OOM超内存问题
import util.gx_model_ctr as gx_model_ctr

gx_model_name='gx_lstm'

def getLstm(data):
    mode=data['mode']
    modelType=data['type']
    client_id=data['client_id']
    new_lstm=glstm.gx_lstm()
    if mode=='train':
        gmc=gx_model_ctr.GMC()
        gmc.ensure_path(modelType,gx_model_name,client_id)
        base_dir=gmc.get_base_dir()
        x_train,y_train=dp.getTrainData(data['data_train'])
        data['x_train']=x_train
        data['y_train']=y_train      
        new_lstm.create_lstm(data)
        new_lstm.save_lstm(base_dir)
        print('------train success------')
        result='success'
        res= {'res_train':result}
        K.clear_session()
    if mode =='predict':
        gmc=gx_model_ctr.GMC()
        tag,base_dir=gmc.ensure_model(modelType,gx_model_name,client_id)
        predictX,scaler,m=dp.getTestdata(data['predictX'])
        model=new_lstm.load_lstm(base_dir+'model')
        testPredict=model.predict(predictX)
        res_predict=dp.datatransfrom(testPredict,scaler,m)
        res= {'res_predict':list(res_predict)}
        K.clear_session()
    return res
