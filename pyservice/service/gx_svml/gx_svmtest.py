# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:16:24 2018

@author: Zcy
"""
import os, sys
sys.path = [os.path.dirname(os.path.abspath(__file__))] + sys.path
import gx_svmModel
import util.gx_model_ctr as gx_model_ctr
import schedule
import time
import threading
gx_model_name='svm'
gmc=gx_model_ctr.GMC()
gsm=gx_svmModel.Model()
model={}

def train(data):
    gmc.ensure_path(data['type'],gx_model_name,data['client_id'])
    base_dir=gmc.get_base_dir()
    trainx,trainy =trans2libsvmX(data['train_data'])
    options=data['options']
    try:
        gsm.save_model(trainx,trainy,options,base_dir,data['type'],data['client_id'],gx_model_name)
        train_time,svmModel,ids=gsm.get_model()
        model[ids]={0:train_time,1:svmModel}
        res={'train':str('success')}
    except:
        res={'train':str('error')}
    
    return res

def predict(data):
    testx =getPredict(data['pridict_data'])
    res=gsm.predict(testx,gx_model_name,data['type'],data['client_id'],model)
    return res

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
            
def trans2libsvmX(data):
    res=[]
    trainy=[]
    for datai in data:
        trainx={}
        index=1
        for i in range(len(datai)):
            if i==len(datai)-1:
                trainy.append(float(datai[i]))
            else:
                trainx[index]=float(datai[i])
                index= index +1                
        res.append(trainx)
    return res,trainy
def getPredict(data):
    res=[]
    for datai in data:
        trainx={}
        index=1
        for i in range(len(datai)):
            trainx[index]=float(datai[i])
            index= index +1                
        res.append(trainx)
    return res
def trainANDpredict(data):
    mode=data['mode']
    threading.Thread(target=run_Thread).start()
    if mode=='train':
        res=train(data)
        return res
    elif mode=='predict':
        res=predict(data)
        return res
    else:
        print('please set right mode!')
    
  