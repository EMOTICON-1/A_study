import numpy as np
from tensorflow.keras.datasets import cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# print(x_train.shape)# (50000,32,32,3)
# print(x_test.shape) # (10000,32,32,3)

from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, train_size=0.8, random_state=66, shuffle=True)

x_train = x_train.reshape(40000,32,32,3)/225.
x_test = x_test.reshape(10000,32,32,3)/225.
x_val = x_val.reshape(10000,32,32,3)/225.

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D,Flatten

#2. 모델링
model  = Sequential()
model.add(Conv2D(filters = 10,kernel_size=(5,5), strides=1, padding='same', input_shape = (32,32,3)))
model.add(MaxPool2D(pool_size=(3,3)))
model.add(Flatten())
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(1))


#3. 컴파일, 훈련
model.compile(loss = 'mse', optimizer='adam', metrics = ['mae'])
'''
EarlyStopping
'''
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
modelpath = '../modelcheckpoint/k46_2_cifar10_{epoch:02d}-{val_loss:.4f}.hdf5'
cp = ModelCheckpoint(filepath=modelpath, monitor='val_loss', save_best_only=True, mode='auto')
early_stopping = EarlyStopping(monitor='loss', patience=20, mode='auto') #loss값이 가장낮을 때를 10번 지나갈 때 까지 기다렸다가 stop. mode는 min, max, auto조정가능
hist = model.fit(x_train, y_train, epochs=10, batch_size=1, validation_data= (x_val, y_val), callbacks = [early_stopping,cp])

#4. 평가, 예측
loss, mae = model.evaluate(x_test, y_test)
print("loss : ", loss)
print("mae : ", mae)

y_predict = model.predict(x_test) 
#print(y_predict)

# cnn
# loss :  6.173558235168457
# mae :  2.0689027309417725
# RMSE : 2.4846644
# R2 :  0.2516900640863633

