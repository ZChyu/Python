# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:20:23 2018

@author: Zcy
"""
import os, sys
sys.path = [os.path.dirname(os.path.abspath(__file__))] + sys.path
from gx_svmutil import svm_train,svm_save_model,svm_predict,svm_load_model
import util.gx_model_ctr as gx_model_ctr
import time
class Model:
    def save_model(self,x_data,y_data,options,base_dir,modelType,client_id,gx_model_name):
        model = svm_train(y_data,x_data,options)
        svm_save_model(base_dir,model)
        self.svmModel=model
        self.ids=gx_model_name+'-'+modelType+'-'+client_id
        self.train_time=time.time()
    def get_model(self):
        return self.train_time,self.svmModel,self.ids
        
    def predict(self,x_data,gx_model_name,modelType,client_id,model):
        gmc=gx_model_ctr.GMC()
        tag,base_dir=gmc.ensure_model(modelType,gx_model_name,client_id)
        ids=gx_model_name+'-'+modelType+'-'+client_id
        y_data=[]
        if ids in model:
            print('tag:',"model in Memory")
            p_label, p_acc, p_val = svm_predict(y_data,x_data,model[ids][1])
            res={'p_acc':str(p_acc),'p_label':str(p_label),'p_val':str(p_val)} 
            result=res            
        elif tag==False:
            result={'error:':'please train model !'}
        else:
            print('tag:',"model in file")
            model=svm_load_model(base_dir+'model')
            p_label, p_acc, p_val = svm_predict(y_data,x_data,model)
            res={'p_acc':str(p_acc),'p_label':str(p_label),'p_val':str(p_val)} 
            result=res                       
        return result