import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

labels = ["role", 'isStarting', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
class_names = ['pres', 'vp', 'va', 'ass']

train_path = open('trainData.csv')
test_path = open('evalData.csv')

train = pd.read_csv(train_path, names=labels, header=0)
test = pd.read_csv(test_path, names=labels, header=0)

train_y = train.pop('role')
test_y = test.pop('role')

model = keras.Sequential([
    keras.layers.Dense(14, activation='relu'),  # hidden layer (2)
    keras.layers.Dense(4, activation='softmax') # output layer (3)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train, train_y, epochs=2)  # we pass the data, labels and epochs and watch the magic!

test_loss, test_acc = model.evaluate(test,  test_y, verbose=1)

print('Test accuracy:', test_acc)

model.save_weights('kerasModel')
