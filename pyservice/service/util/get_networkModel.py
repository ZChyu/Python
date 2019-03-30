# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:20:23 2018

@author: Zcy
"""
import util.gx_network as networks
import util.gx_model_ctr as gx_model_ctr
import time
class Model:
    def save_model(self,structs,x_data,y_data,train_epoches,base_dir,modelType,client_id,gx_model_name):
        network=networks.GX_network()
        network.createNetwork(structs)
        self.loss=network.train(x_data,y_data,train_epoches)
        network.save_network(base_dir)
        self.network=network
        self.ids=gx_model_name+'-'+modelType+'-'+client_id
        self.train_time=time.time()
    def get_model(self):
        return self.train_time,self.network,self.loss,self.ids
        
    def prdict(self,x_data,gx_model_name,modelType,client_id,model):
        gmc=gx_model_ctr.GMC()
        tag,base_dir=gmc.ensure_model(modelType,gx_model_name,client_id)
        ids=gx_model_name+'-'+modelType+'-'+client_id
        if ids in model:
            print('tag:',"model in Memory")
            res = model[ids][1].predict(x_data) 
            result=res.tolist()                 
        elif tag==False:
            result={'error:':'please train model !'}
        else:
            print('tag:',"model in file")
            network=networks.GX_network()
            network.load_network(base_dir+'model')
            res=network.predict(x_data)
            result=res.tolist()
            
        return result