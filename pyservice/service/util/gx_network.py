# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 13:01:38 2018

@author: Lidh
"""
import tensorflow as tf
class GX_network:
    def getActivationFunction(self,act):
        if act==0:
            return None
        if act==1:
            return tf.nn.softplus
        if act==2:
            return tf.nn.softmax
        if act==3:
            return tf.nn.softsign
        if act==4:
            return tf.nn.tanh
        if act==5:
            return tf.nn.sigmoid
        if act==6:
            return tf.nn.relu
        if act==7:
            return tf.nn.relu6
        return None
    def add_layer(self,inputs,in_size,out_size,activation_function=None,seed=None):
        if seed==None:
            w=tf.Variable(tf.random_normal([in_size,out_size]))
        else:
            w=tf.Variable(tf.random_normal([in_size,out_size], seed=float(seed)))
        #w=tf.Variable(tf.zeros([in_size,out_size]))
        b=tf.Variable(tf.zeros([1,out_size])+0.1)
        Wx_plus_b=tf.matmul(inputs,w)+b
        if activation_function is None:
            outputs=Wx_plus_b
        else:
            outputs=activation_function(Wx_plus_b)
        return outputs
    def predict(self,x_data):
        res=self.sess.run(self.predition,feed_dict={self.xs:x_data})
        return res
    def createNetwork(self,structs):
        input_ps=structs['input_ps']
        layers=structs['layers']
        learn_rate=structs['learn_rate']
        tf.reset_default_graph()
        lay_nums=len(layers)
        if lay_nums<2:
            raise RuntimeError('lar_num Error')
        last_ps=input_ps
        self.xs=tf.placeholder(tf.float32,[None,last_ps],name='xs') #last_ps列 行不确定
        last_output=self.xs
        for layer in layers:
            lay=self.add_layer(last_output,last_ps,layer['ps'],self.getActivationFunction(layer['act']))
            last_output=lay
            #print(layer)
            last_ps=layer['ps']
        self.global_step = tf.Variable(0)
        learning_rate = tf.train.exponential_decay(learn_rate,self.global_step,100,0.96,staircase=True)
        self.predition=last_output
        self.ys=tf.placeholder(tf.float32,[None,last_ps],name='ys')
        self.loss=tf.sqrt(tf.reduce_mean(tf.reduce_sum(tf.square(self.ys-self.predition),reduction_indices=[1])))
        #self.loss=tf.reduce_mean(tf.square(self.ys-self.predition))
        #tf.reduce_sum按列求和
        self.train_gx=tf.train.GradientDescentOptimizer(learning_rate).minimize(self.loss,global_step = self.global_step)       
        init=tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)
    def save_network(self,base_dir):
        tf.add_to_collection('loss', self.loss)  
        tf.add_to_collection('predition', self.predition)
        tf.add_to_collection('train_gx', self.train_gx)
        saver = tf.train.Saver()
        saver.save(self.sess,save_path=base_dir)
    def load_network(self,base_dir):
        tf.reset_default_graph()  
        self.sess=tf.Session()
        saver = tf.train.import_meta_graph(base_dir+'.meta')
        saver.restore(self.sess,base_dir)
        self.predition=tf.get_collection('predition')[0]    
        self.loss=tf.get_collection('loss')[0] 
        self.train_gx=tf.get_collection('train_gx')[0] 
        graph = tf.get_default_graph()
        self.xs = graph.get_operation_by_name('xs').outputs[0]
        self.ys = graph.get_operation_by_name('ys').outputs[0]
    def train(self,x_data,y_data,train_times,is_print=False):
        for i in range(train_times):
            self.sess.run(self.train_gx,feed_dict={self.xs:x_data,self.ys:y_data})
            if is_print and (i+1)%50 == 0:
                print('epoch:'+str(i)+',error:'+str(self.sess.run(self.loss,feed_dict={self.xs:x_data,self.ys:y_data})/100))
        return self.sess.run(self.loss,feed_dict={self.xs:x_data,self.ys:y_data})/100
