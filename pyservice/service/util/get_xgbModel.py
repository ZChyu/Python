# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 15:05:29 2018

@author: Zcy
"""
import xgboost as xgb
import util.gx_model_ctr as gx_model_ctr
import time
import numpy as np
class Model:
    def save_model(self,x_data,y_data,params,numRounds,base_dir,modelType,client_id,gx_model_name):
        trainData=xgb.DMatrix(x_data,label=y_data)
        model=xgb.train(params,trainData,numRounds)
        model.save_model(base_dir)
        self.xgbModel=model
        self.ids=gx_model_name+'-'+modelType+'-'+client_id
        self.train_time=time.time()
    def get_model(self):
        return self.train_time,self.xgbModel,self.ids
        
    def prdict(self,x_data,gx_model_name,modelType,client_id,Model,params):
        gmc=gx_model_ctr.GMC()
        tag,base_dir=gmc.ensure_model(modelType,gx_model_name,client_id)
        ids=gx_model_name+'-'+modelType+'-'+client_id
        if ids in Model:
            print('tag:',"model in Memory")
            ypred = Model[ids][1].predict(xgb.DMatrix(x_data))
            ypred=np.array(ypred).astype(np.str)
            result={"code":200,"result":list(ypred)}                 
        elif tag==False:
            result={'error:':'please train model !'}
        else:
            print('tag:',"model in file")
            model=xgb.Booster(params)
            model.load_model(base_dir+'model')
            ypred = model.predict(xgb.DMatrix(x_data))
            ypred=np.array(ypred).astype(np.str)
            result={"code":200,"result":list(ypred)}
            
        return result