# r2_score
from sklearn.datasets import load_iris
import tensorflow as tf

dataset = load_iris()
x_data = dataset.data
y_data = dataset.target
y_data = y_data.reshape(-1,1)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.8)
print(x_data.shape) #(150, 4)
print(y_data.shape) #(150, 1)

from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# 원-핫 인코딩 적용
encoder = OneHotEncoder()
encoder.fit(y_test)
y_test = encoder.transform(y_test)
encoder.fit(y_train)
y_train = encoder.transform(y_train)
y_test=y_test.toarray()
y_train=y_train.toarray()
print(y_test.shape)
print(type(y_test)) #<class 'scipy.sparse.csr.csr_matrix'>


x = tf.placeholder('float', [None, 4])
y = tf.placeholder('float', [None, 3])

w = tf.Variable(tf.random_normal([4, 3]), name = 'weight')
b = tf.Variable(tf.random_normal([1, 3]), name = 'bias')

hypothesis = tf.nn.softmax(tf.matmul(x, w) + b)
# loss = tf.reduce_mean(tf.square(hypothesis-y)) #mse
from sklearn.metrics import r2_score, accuracy_score
loss = tf.reduce_mean(-tf.reduce_sum(y * tf.log(hypothesis), axis = 1)) #categorical_crossentropy
optimizer = tf.train.AdamOptimizer(learning_rate=0.4).minimize(loss)
with tf.Session() as sess:  
    sess.run(tf.global_variables_initializer())

    for step in range(2001):    
        _, cost_val = sess.run([optimizer, loss], feed_dict={x:x_train, y:y_train})
        if step % 200 == 0 : 
            print(step, cost_val)
    
    a = sess.run(hypothesis, feed_dict={x:x_test})
    print("acc: ",accuracy_score(sess.run(tf.argmax(y_test,1)),sess.run(tf.argmax(a,1))))


# sess.close()

# GradientDescentOptimizer(learning_rate=0.01)
# acc:  0.9333333333333333
# AdamOptimizer(learning_rate=0.01)
# acc:  0.9666666666666667
