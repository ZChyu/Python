# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 11:20:56 2018

@author: Zcy
"""
import time
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from util import gx_network
import util.gx_model_ctr as gx_model_ctr
import util.get_networkModel as getModel
import schedule
import threading

gx_model_name='gx_network'
model={}

def train_one(x_data,y_data,learn_rate,layers,train_epoches,modelType,client_id):
    gmc=gx_model_ctr.GMC()
    gmc.ensure_path(modelType,gx_model_name,client_id)
    base_dir=gmc.get_base_dir()
    x_data=np.array(x_data)
    y_data=np.array(y_data)
    structs={'input_ps':x_data[0].size,'learn_rate':learn_rate,'layers':layers}
    get_model=getModel.Model()
    get_model.save_model(structs,x_data,y_data,train_epoches,base_dir,modelType,client_id,gx_model_name)
    train_time,network,loss,ids=get_model.get_model()
    model[ids]={0:train_time,1:network}#保存模型
    return loss
def train_two(x_data,y_data,train_epoches,modelType,client_id):
    gmc=gx_model_ctr.GMC()
    gmc.ensure_path(modelType,gx_model_name,client_id)
    base_dir=gmc.get_base_dir()
    network=gx_network.GX_network()
    network.load_network(base_dir)
    loss=network.train(x_data,y_data,train_epoches)
    network.save_network(base_dir)
    ids=gx_model_name+'-'+modelType+'-'+client_id
    train_time=time.time()
    model[ids]={0:train_time,1:network}
    return loss

def predict(x_data,modelType,client_id):
    get_model=getModel.Model()
    result=get_model.prdict(x_data,gx_model_name,modelType,client_id,model)      
    return result
           
def clear_model():#清除模型
    clear_time=time.time()
    delta=30
    for key in list(model.keys()):
        if clear_time>=model[key][0]+delta:
            del model[key]
            print('clear success')
        else:
            pass
    
def run_Thread():#同步清除
    schedule.every(5).seconds.do(clear_model)   
    while True:
            schedule.run_pending()
            time.sleep(2)
   
def getJson(data):
 #   print(data)
    modelType=data['type']
    client_id=data['client_id']
    x_data=data["x_data"]
    mode=data['mode']
    threading.Thread(target=run_Thread).start()
    if mode=='train_one':
        y_data=np.transpose([data["y_data"]])
        learn_rate=float(data['learn_rate'])
        train_epoches=int(data['train_epoches'])
        layers=np.array(data['layers'])
        res=train_one(x_data,y_data,learn_rate,layers,train_epoches,modelType,client_id)
        res={'json':res}
    elif mode=='train_two':
        y_data=np.transpose([data["y_data"]])
        train_epoches=int(data['train_epoches'])
        res=train_two(x_data,y_data,train_epoches,modelType,client_id)
        res={'json':res}
    elif mode=='predict':
        res=predict(x_data,modelType,client_id)
        res={'json':str(res)}
    else:
        res={"json":'please set right mode!'}
    return res
