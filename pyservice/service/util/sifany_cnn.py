
import tensorflow as tf
import numpy as np
class Sifany_cnn:
    def __init__(self):
        self.graph=tf.Graph()
    def weight_variable(self,shape):
        initial = tf.truncated_normal(shape,stddev=0.1);
        return tf.Variable(initial)
    def bias_variable(self,shape):
        initial = tf.constant(0.1,shape=shape)
        return tf.Variable(initial)
    def conv2d(self,x,w):
        return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding='SAME')#卷积层
    def max_pool_2_2(self,x):
    	# 池化卷积结果（conv2d）池化层采用kernel大小为2*2，步数也为2，周围补0，取最大值。数据量缩小了4倍
        return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')#池化层
        #x:需要池化的输入，一般池化层接在卷积层后面，所以输入通常是feature map，依然是[batch, height, width, channels]这样的shape
 		#ksize：池化窗口的大小，取一个四维向量，一般是[1, height, width, 1]，因为我们不想在batch和channels上做池化，所以这两个维度设为了1
 		#strides：和卷积类似，窗口在每一个维度上滑动的步长，一般也是[1, stride,stride, 1]
 		#padding：和卷积类似，可以取'VALID' 或者'SAME'
 		#返回一个Tensor，类型不变，shape仍然是[batch, height, width, channels]这种形式
    def create(self,win_size,pass_size=8):#pass_size：卷积核个数
        tf.reset_default_graph()
        win_size2=int(win_size/4)
        self.x = tf.placeholder("float",shape=[None,win_size*win_size],name='x')
        self.y_ = tf.placeholder("float",shape=[None,2],name='y')
        # 第一层卷积操作
        w_conv1 = self.weight_variable([5,5,1,pass_size])#卷积核尺寸，图像通道数，卷积核个数
        b_conv1 = self.bias_variable([pass_size])#偏置量，pass_size:卷积核个数
        x_image = tf.reshape(self.x,[-1,win_size,win_size,1])#win_size图片尺寸，-1代表图片数量不定
        h_conv1 = tf.nn.relu(self.conv2d(x_image,w_conv1) + b_conv1)## 图片乘以卷积核，并加上偏执量
        h_pool1 = self.max_pool_2_2(h_conv1)
        # 第二层卷积操作
        w_conv2 = self.weight_variable([5,5,pass_size,64])
        b_conv2 = self.bias_variable([64])
        h_conv2 = tf.nn.relu(self.conv2d(h_pool1,w_conv2) + b_conv2)
        h_pool2 = self.max_pool_2_2(h_conv2)
        # 第三层全连接操作 
        w_fc1 = self.weight_variable([win_size2*win_size2*64,1024])
        b_fc1 = self.bias_variable([1024])
        h_pool2_flat = tf.reshape(h_pool2,[-1,win_size2*win_size2*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,w_fc1) + b_fc1)
        self.keep_prob = tf.placeholder("float",name='keep_prob')
        h_fc1_drop = tf.nn.dropout(h_fc1,self.keep_prob)
        # 第四层输出操作
        w_fc2 = self.weight_variable([1024,2])
        b_fc2 = self.bias_variable([2])
        self.y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop,w_fc2) + b_fc2)
        # 定义loss(最小误差概率)，选定优化优化loss
        cross_entropy = -tf.reduce_sum(self.y_ * tf.log(self.y_conv))
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        #开始数据训练以及评测
        correct_prediction = tf.equal(tf.argmax(self.y_conv,1),tf.argmax(self.y_,1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction,"float"))
        self.sess = tf.Session()
        self.sess.run(tf.initialize_all_variables())
    def train2(self,x_data,y_data):
        train_accuracy = self.accuracy.eval(session=self.sess,feed_dict={self.x:x_data,self.y_:y_data,self.keep_prob:1.0})
        print("step,training accuracy %g"%(train_accuracy))
        self.train_step.run(session = self.sess,feed_dict={self.x:x_data,self.y_:y_data,self.keep_prob:0.5})
    def train(self,x_data_0,y_data_0,batch_size,train_times=10):
        for i in range(0,len(x_data_0),batch_size):
            for j in range(train_times):
                x_data=np.array(x_data_0[i:i+batch_size])
                y_data=np.array(y_data_0[i:i+batch_size])
                train_accuracy = self.accuracy.eval(session=self.sess,feed_dict={self.x:x_data,self.y_:y_data,self.keep_prob:1.0})
                print("step %d,training accuracy %g"%(i,train_accuracy))
                self.train_step.run(session = self.sess,feed_dict={self.x:x_data,self.y_:y_data,self.keep_prob:0.5})
    def predict(self,x_data):
        return self.y_conv.eval(session=self.sess,feed_dict={self.x:x_data,self.keep_prob:1.0})
    def save_network(self,base_dir):
        tf.add_to_collection('train_step', self.train_step)
        tf.add_to_collection('accuracy', self.accuracy)
        tf.add_to_collection('y_conv', self.y_conv)
        saver = tf.train.Saver()
        saver.save(self.sess,save_path=base_dir)
    def load_network(self,base_dir):
        with self.graph.as_default():
            self.saver = tf.train.import_meta_graph(base_dir+'.meta')
        self.sess=tf.Session(graph=self.graph)
        with self.sess.as_default():
            with self.graph.as_default():
                self.saver.restore(self.sess,base_dir)
                self.y_conv=tf.get_collection('y_conv')[0]    
                self.accuracy=tf.get_collection('accuracy')[0] 
                self.train_step=tf.get_collection('train_step')[0] 
                graph = tf.get_default_graph()
                self.x = graph.get_operation_by_name('x').outputs[0]
                self.y_ = graph.get_operation_by_name('y').outputs[0]
                self.keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]

 
