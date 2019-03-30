# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 16:32:14 2018

@author: Zcy
"""
import numpy as np
from sklearn.preprocessing import MinMaxScaler
np.random.seed(1)  # Fix random seed for reproducibility/设定随机种子，保证实验可复现

def getTrainData(data):
         #  dataset = dataframe.iloc[:, [1, 2, 3, 4, 5, 6,7]].values#通过索引取值
        # Normalize the dataset/标准化数据集
    scaler = MinMaxScaler(feature_range=(0, 1))#归一化处理：调高计算精度
    dataset = scaler.fit_transform(data)#fit_transform()的作用就是先拟合数据，然后转化它将其转化为标准形式
    trainX, trainY = [], []
    for i in range(len(dataset)-1):
        a = dataset[i:(i + 1), 1:dataset.shape[1]]
        trainX.append(a)
        trainY.append(dataset[i, 0])
    trainXX=np.array(trainX)
    trainYY=np.array(trainY)
    trainXX=np.reshape(trainXX, (trainXX.shape[0], dataset.shape[1]-1, trainXX.shape[1]))
    return trainXX, trainYY
    
def getTestdata(test_data):
    scaler = MinMaxScaler(feature_range=(0, 1))#归一化处理：调高计算精度
    dataset = scaler.fit_transform(test_data)#fit_transform()的作用就是先拟合数据，然后转化它将其转化为标准形式
    trainX= []
    for i in range(len(dataset)-1):
        a = dataset[i:(i + 1), 0:dataset.shape[1]]
        trainX.append(a)
    trainXX=np.array(trainX)
    trainXX=np.reshape(trainXX, (trainXX.shape[0], dataset.shape[1], trainXX.shape[1]))
    return trainXX,scaler,dataset.shape[1]
   
def datatransfrom(testPredict,scaler,m):
#        # Inverse transform and then select the right field/数据转换
    testPredict_dataset_like = np.zeros(shape=(len(testPredict),m))
    testPredict_dataset_like[:, 0] = testPredict[:, 0]
    testPredict = scaler.inverse_transform(testPredict_dataset_like)[:, 0]

    return testPredict



    

