# -*- coding:utf-8 -*-
'''
Time: 2018/9/18 15:36
Author: Bangpeng
'''
import tensorflow as tf
import numpy as np
import pickle

class kmeans(object):

    def __init__(self):

        self.x=tf.placeholder(tf.float32, [None, None])
        self.cl=tf.placeholder(tf.float32, [None, None])

        cl2=tf.expand_dims(tf.transpose(self.cl), 0)
        x2=tf.expand_dims(self.x,-1)
        cl2=tf.tile(cl2,[tf.shape(self.x)[0]]+[1]*len(self.cl.get_shape().as_list()) )
        x2=tf.tile(x2,[1]*len(self.x.get_shape().as_list())+[tf.shape(self.cl)[0]])

        dis=tf.reduce_sum(tf.square(x2-cl2),1)
        dis=tf.to_float(tf.equal(dis-tf.expand_dims(tf.reduce_min(dis,1),1), 0.))
        self.laber=tf.argmax(dis,1)
        self.fcl=tf.matmul(tf.div(dis,tf.reduce_sum(dis,0)),self.x,True)

    def predict(self, data, c):

        assert type(data) in [list, np.array, np.ndarray], 'Input data must be a list or an array'
        assert len(np.shape(data))>1, 'Input data shape must be at least 2-D'
        data = np.reshape(data,[-1,np.prod(np.shape(data)[1:])])
        assert type(c) in [list, np.array, np.ndarray], 'Input c must be a list or an array'
        c = np.reshape(c,[-1,np.prod(np.shape(c)[1:])])

        dl=None
        with tf.Session() as sess:
            dl=sess.run(self.laber,feed_dict={self.x:data,self.cl:c})
        return dl

    def fit(self, data, c, times_limit=-1, cnum=None):
        assert type(data) in [list, np.array, np.ndarray], 'Input data must be a list or an array'
        assert len(np.shape(data))>1, 'Input data shape must be at least 2-D'
        data = np.reshape(data,[-1,np.prod(np.shape(data)[1:])])
        assert type(c) in [list, np.array, np.ndarray, str], 'Input c must be a list or an array or \'random\''
        if type(c) is str and c is 'random':
            assert type(cnum) is int, 'Input cnum must be an int'
            c=[data[int(np.random.random()*(len(data)-1))] for i in range(cnum)]
        else:
            c = np.reshape(c,[-1,np.prod(np.shape(c)[1:])])

        nc,c,dl,times = c,None,None,0
        while (not np.all(np.equal(np.array(nc),np.array(c)))) and (times_limit==-1 or times<times_limit):
            c, times = nc, times+1
            with tf.Session() as sess:
                nc,dl=sess.run([self.fcl,self.laber],feed_dict={self.x:data,self.cl:nc})
        return nc,dl

def getJson(data):
    x_data=data["data"]
    k=kmeans()
    baseDir = data["modelPath"]
    if data["mode"] == "train":
        cnum1=int(data["classNum"])
        cc,dl=k.fit(np.array(x_data),c='random', cnum=cnum1)
        f = open(baseDir, "wb")
        pickle.dump(cc, f)
        f.close()
        res = []
        for l in range(cnum1):
            res.append("class " + str(l) + " percent is " + str(round(list(dl).count(l)/len(dl), 2)))
        res={'result':res}
        return res
    elif data["mode"] == "predict":
        f = open(baseDir, "rb")
        cc=pickle.load(f)
        f.close()
        res=k.predict(x_data,cc)
        res={'result':str(res)}
        return res
    else:
        return({'result':"Please input right mode!"})
