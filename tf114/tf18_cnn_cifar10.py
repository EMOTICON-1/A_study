import tensorflow as tf
import numpy as np
# tf.set_random_seed(66)

tf.compat.v1.disable_eager_execution()
print(tf.executing_eagerly()) # False

print(tf.__version__) #2.3.1

#1.
from tensorflow.keras.datasets import cifar10
(x_train, y_train),(x_test, y_test) = cifar10.load_data() 

from tensorflow.keras.utils import to_categorical   
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

print(x_train.shape, y_train.shape) #(50000, 32, 32, 3) (50000, 10)
x_train = x_train.reshape(50000,32,32,3).astype('float32')/255
x_test = x_test.reshape(10000,32,32,3).astype('float32')/255

learning_rate = 0.001
training_epochs = 15
batch_size = 100
total_batch = int(len(x_train)/batch_size)

x = tf.compat.v1.placeholder(tf.float32, [None, 32, 32, 3])
y = tf.compat.v1.placeholder(tf.float32, [None, 10])

#2.
#L1
w1 = tf.compat.v1.get_variable('w1', shape = [3, 3, 3, 64])
L1 = tf.nn.conv2d(x, w1, strides=[1,1,1,1], padding ='SAME')
print(L1) #Tensor("Conv2D:0", shape=(?, 28, 28, 32), dtype=float32)
# Conv2D(32,(3,3), input_shape(28, 28, 1))
L1 = tf.nn.relu(L1)
L1 = tf.nn.max_pool(L1, ksize=[1,2,2,1],strides=[1,2,2,1], padding = 'SAME')
print(L1) #Tensor("MaxPool:0", shape=(?, 14, 14, 32), dtype=float32)
#L2
w2 = tf.compat.v1.get_variable('w2', shape = [3, 3, 64, 64])
L2 = tf.nn.conv2d(L1, w2, strides=[1,1,1,1], padding ='SAME')
L2 = tf.nn.selu(L2)
L2 = tf.nn.max_pool(L2, ksize=[1,2,2,1],strides=[1,2,2,1], padding = 'SAME')
print(L2) #Tensor("MaxPool_1:0", shape=(?, 7, 7, 64), dtype=float32)
#L3
w3 = tf.compat.v1.get_variable('w3', shape = [3, 3, 64, 128])
L3 = tf.nn.conv2d(L2, w3, strides=[1,1,1,1], padding ='SAME')
L3 = tf.nn.relu(L3)
L3 = tf.nn.max_pool(L3, ksize=[1,2,2,1],strides=[1,2,2,1], padding = 'SAME')
print(L3) #Tensor("MaxPool_2:0", shape=(?, 4, 4, 128), dtype=float32)
#L4
w4 = tf.compat.v1.get_variable('w4', shape = [3, 3, 128, 64])
L4 = tf.nn.conv2d(L3, w4, strides=[1,1,1,1], padding ='SAME')
L4 = tf.nn.selu(L4)
L4 = tf.nn.max_pool(L4, ksize=[1,2,2,1],strides=[1,2,2,1], padding = 'SAME')
print(L4) #Tensor("MaxPool_3:0", shape=(?, 2, 2, 64), dtype=float32)
#Flatten
L_flat = tf.reshape(L4, [-1,2*2*64])
print(L_flat) #Tensor("Reshape:0", shape=(?, 256), dtype=float32)
#L5
w5 = tf.compat.v1.get_variable('w5', shape = [2*2*64, 64])#, initializer=tf.contrib.layers.xavier_initializer())    
b5 = tf.Variable(tf.compat.v1.random_normal([64]), name='b1')
L5 = tf.nn.relu(tf.matmul(L_flat, w5)+ b5)
# L5 = tf.nn.dropout(L5, keep_prob=0.2)
print(L5) #Tensor("dropout/mul_1:0", shape=(?, 64), dtype=float32)
#L6
w6 = tf.compat.v1.get_variable('w6', shape = [64, 32])#, initializer=tf.contrib.layers.xavier_initializer())    
b6 = tf.Variable(tf.compat.v1.random_normal([32]), name='b6')
L6 = tf.nn.relu(tf.matmul(L5, w6)+ b6)
# L6 = tf.nn.dropout(L6, keep_prob=0.2)
print(L6) #Tensor("dropout/mul_1:0", shape=(?, 64), dtype=float32)
#L7
w7 = tf.compat.v1.get_variable('w7', shape = [32, 10])#, initializer=tf.contrib.layers.xavier_initializer())    
b7 = tf.Variable(tf.compat.v1.random_normal([10]), name='b7')
hypothesis = tf.nn.softmax(tf.matmul(L6, w7)+ b7)
print("최종출력 : ", hypothesis)

#3  
loss = tf.reduce_mean(-tf.reduce_sum(y*tf.math.log(hypothesis), axis=1))
optimizer = tf.compat.v1.train.AdamOptimizer(1e-3).minimize(loss)

#4  
sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())

for epoch in range(training_epochs): 
    avg_loss = 0

    for i in range(total_batch): #600번    # 딱 떨어지지 않는 데이터는 버려진다
        start = i * batch_size
        end = start + batch_size
        batch_x, batch_y = x_train[start:end], y_train[start:end]
        feed_dict = {x:batch_x, y:batch_y}
        c, _ = sess.run([loss,optimizer], feed_dict = feed_dict)
        avg_loss += c/total_batch

    print('Epoch : ', '%04d' %(epoch + 1), 'loss = {:.9f}'.format(avg_loss))

print('훈련끝')

prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(prediction,tf.float32))

print('acc : ', sess.run(accuracy, feed_dict = {x:x_test, y:y_test}))