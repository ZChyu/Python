# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:27:23 2018

@author: Zcy
"""
import time
import numpy as np
from keras.models import Sequential,load_model
from keras.layers import LSTM, Dense

np.random.seed(1)  # Fix random seed for reproducibility/设定随机种子，保证实验可复现
class gx_lstm():
    # Create and fit the LSTM network/创建并拟合LSTM网络
    def create_lstm(self,data):
        self.num_neur=data['num_neur']
        self.look_back=data['look_back']
        self.x_train=data['x_train']
        self.y_train=data['y_train']
        self.epochs=data['epochs']
        self.batch_size=data['batch_size']
        self.activation=data['activation']
        start_cr_a_fit_net = time.time()

        self.LSTM_model = Sequential()
        for i in range(len(self.num_neur)):  # 构建多层网络
            if len(self.num_neur) == 1:
                self.LSTM_model.add(LSTM(self.num_neur[i], input_shape=(None, self.look_back)))
            else:
                if i < len(self.num_neur) - 1:
                    self.LSTM_model.add(LSTM(self.num_neur[i], input_shape=(None, self.look_back), return_sequences=True))
                else:
                    self.LSTM_model.add(LSTM(self.num_neur[i], input_shape=(None, self.look_back)))

        self.LSTM_model.add(Dense(1, activation=self.activation))
        self.LSTM_model.summary()  # Summary the structure of neural network/网络结构总结
        self.LSTM_model.compile(loss='mean_squared_error', optimizer='adam')  # Compile the neural network/编译网络
        self.LSTM_model.fit(self.x_train, self.y_train, epochs=self.epochs, batch_size=self.batch_size
                       , verbose=0)  # Fit the LSTM network/拟合LSTM网络
        end_cr_a_fit_net = time.time() - start_cr_a_fit_net
        print('Running time of creating and fitting the LSTM network: %.2f Seconds' % (end_cr_a_fit_net))
    def save_lstm(self,base_dir):
        self.LSTM_model.save(base_dir)
    
    def load_lstm(self,base_dir):
        return load_model(base_dir)
    
    def predict(self,x_data):
        testPredict = self.LSTM_model.predict(x_data)  # Predict by test data set/测试集预测
        return testPredict