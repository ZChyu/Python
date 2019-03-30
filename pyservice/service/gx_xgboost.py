# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:16:24 2018

@author: Zcy
"""
import json
import numpy as np 
import pandas as pd
import schedule
import time
import threading    
import util.gx_model_ctr as gx_model_ctr
import util.get_xgbModel as get_xgbModel
gx_model_name='gx_xgboost'
gmc=gx_model_ctr.GMC()
get_xgb=get_xgbModel.Model()
Models={}

def clear_model():#清除模型
    clear_time=time.time()
    delta=30
    for key in list(Models.keys()):
        if clear_time>=Models[key][0]+delta:
            del Models[key]
            print('clear success')
        else:
            pass
    
def run_Thread():#同步清除
    schedule.every(5).seconds.do(clear_model)   
    while True:
            schedule.run_pending()
            time.sleep(2)
def getXgboost(data):
    threading.Thread(target=run_Thread).start()
    if data!=None:
        x_data=data["x_data"]
        x_data=np.array(x_data)
        x_data=x_data.astype(float)
        x_data=pd.DataFrame(x_data)

        mode=data["mode"]
        params=data["params"]
        modelType=data['type']
        client_id=data['client_id']
        if mode=="train":
            gmc.ensure_path(modelType,gx_model_name,client_id)
            base_dir=gmc.get_base_dir()
            y_data=data["y_data"]
            y_data=np.array(y_data).astype(np.int32)
            y_data=pd.DataFrame(np.array(y_data))
            numRounds=data["numRounds"]
            get_xgb.save_model(x_data,y_data,params,numRounds,base_dir,modelType,client_id,gx_model_name)
            train_time,xgbModel,ids=get_xgb.get_model()
            Models[ids]={0:train_time,1:xgbModel}
            res={"code":200,"result":"train model over!"}
        if mode=="predict":       
            res=get_xgb.prdict(x_data,gx_model_name,modelType,client_id,Models,params)
        return (res)
    else:
        content = json.dumps({"error_code":"1001"})  
        resp = (content)
        return resp 