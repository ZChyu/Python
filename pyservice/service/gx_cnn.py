# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 14:31:05 2019

@author: Zcy
"""
from util import sifany_cnn
def getCNN(Data):
    shape=Data['shape']
    CNN=sifany_cnn.Sifany_cnn(shape)
    
    win_size=Data['win_size']
    x_data=Data['x_data']
    y_data=Data['y_data']
    base_dir=Data['base_dir']
    batch_size=Data['batch_size']
    x_data_0=Data['x_data_0']
    y_data_0=Data['y_data_0']
    mode=Data['mode']
    if mode=='train':
        CNN.create(win_size)
        CNN.train(x_data_0,y_data_0,batch_size)
        CNN.save_network(base_dir)
        res={"res":'train success !'}
    elif mode=='predict':
        CNN.create(win_size)
        CNN.train(x_data,y_data)
        CNN.save_network(base_dir)
    elif mode=='predict':
        CNN.load_network(base_dir)
        res=CNN.predict(x_data)
    else:
        res={"res":'please input right mode !'}
    return res
        
    