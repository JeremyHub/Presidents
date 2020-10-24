import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

# apply the z-score method in Pandas using the .mean() and .std() methods
def z_score(df):
    # copy the dataframe
    df_std = df.copy()
    # apply the z-score method
    for column in df_std.columns:
        df_std[column] = (df_std[column] - df_std[column].mean()) / df_std[column].std()
    return df_std

def upperOrLower(num):
    if num < 2:
        return 0
    elif num >= 2:
        return 1

def compressToUpperLower(df):
    data = df.copy()
    data = data.map(upperOrLower)
    return data

labels = ["role", 'isStarting', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
# class_names = ['pres', 'vp', 'va', 'ass']
class_names = ['upper', 'lower']

train_path = open('trainData.csv')
test_path = open('evalData.csv')

trainPreNorm = pd.read_csv(train_path, names=labels, header=0)
testPreNorm = pd.read_csv(test_path, names=labels, header=0)

train_y = compressToUpperLower(trainPreNorm.pop('role'))
test_y = compressToUpperLower(testPreNorm.pop('role'))

# train_y = trainPreNorm.pop('role')
# test_y = testPreNorm.pop('role')

train = z_score(trainPreNorm)
test = z_score(testPreNorm)

model = keras.Sequential([
    keras.layers.Dense(50, activation='relu'),  # hidden layer (2)
    keras.layers.Dense(50, activation='relu'),  # hidden layer (2)

    keras.layers.Dense(2, activation='softmax')  # output layer (3)
    # keras.layers.Dense(4, activation='softmax')  # output layer (3)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train, train_y, epochs=2)

test_loss, test_acc = model.evaluate(test,  test_y, verbose=1)

print('Test accuracy:', test_acc)

model.save('kerasModelUpperLower')
