import numpy as np
import tensorflow as tf
import autokeras as ak
from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(60000,28,28,1).astype('float32')/255.
x_test = x_test.reshape(10000,28,28,1).astype('float32')/255.

from tensorflow.keras.utils import to_categorical
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

from tensorflow.keras.models import load_model

model = load_model('C:/data/test_auto/save/aaa.h5')
model.summary()

best_model = load_model('C:/data/test_auto/save/best_aaa.h5')
best_model.summary()

results = model.evaluate(x_test, y_test)
print(results)
# [0.05835721269249916, 0.9797000288963318]
best_results = best_model.evaluate(x_test, y_test)
print(best_results)
# [0.05835721269249916, 0.9797000288963318]
