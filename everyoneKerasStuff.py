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

def concat(str1, str2):
    return str(str1) + str(str2)

labels = ['role0', 'isStarting0', '2(0)', '3(0)', '4(0)', '5(0)', '6(0)', '7(0)', '8(0)', '9(0)', '10(0)', '11(0)', '12(0)', '13(0)', '14(0)',
            'role1', 'isStarting1', '2(1)', '3(1)', '4(1)', '5(1)', '6(1)', '7(1)', '8(1)', '9(1)', '10(1)', '11(1)', '12(1)', '13(1)', '14(1)',
            'role2', 'isStarting2', '2(2)', '3(2)', '4(2)', '5(2)', '6(2)', '7(2)', '8(2)', '9(2)', '10(2)', '11(2)', '12(2)', '13(2)', '14(2)',
            'role3', 'isStarting3', '2(3)', '3(3)', '4(3)', '5(3)', '6(3)', '7(3)', '8(3)', '9(3)', '10(3)', '11(3)', '12(3)', '13(3)', '14(3)']

class_names = ['0123', '0132', '0231', '0213', '0312', '0321',
               '1023', '1032', '1230', '1203', '1302', '1320',
               '2103', '2130', '2031', '2013', '2310', '2301',
               '3120', '3102', '3201', '3210', '3012', '3021', ]

class_dict = {  '0123':0,
                '0132':1,
                '0231':2,
                '0213':3,
                '0312':4,
                '0321':5,
                '1023':6,
                '1032':7,
                '1230':8,
                '1203':9,
                '1302':10,
                '1320':11,
                '2103':12,
                '2130':13,
                '2031':14,
                '2013':15,
                '2310':16,
                '2301':17,
                '3120':18,
                '3102':19,
                '3201':20,
                '3210':21,
                '3012':22,
                '3021':23,
}

train_path = open('everyoneTrainData.csv')
test_path = open('everyoneEvalData.csv')

trainPreNorm = pd.read_csv(train_path, names=labels, header=0)
testPreNorm = pd.read_csv(test_path, names=labels, header=0)

train_y0 = trainPreNorm.pop('role0').tolist()
test_y0 = testPreNorm.pop('role0').tolist()
train_y1 = trainPreNorm.pop('role1').tolist()
test_y1 = testPreNorm.pop('role1').tolist()
train_y2 = trainPreNorm.pop('role2').tolist()
test_y2 = testPreNorm.pop('role2').tolist()
train_y3 = trainPreNorm.pop('role3').tolist()
test_y3 = testPreNorm.pop('role3').tolist()

testList = []
for i in range(len(test_y0)):
    dataForLine = (str(test_y0[i]) + str(test_y1[i]) + str(test_y2[i]) + str(test_y3[i]))
    testList.append(class_dict.get(dataForLine))

test_y = pd.Series(testList)

trainList = []
for i in range(len(train_y0)):
    dataForLine = (str(train_y0[i]) + str(train_y1[i]) + str(train_y2[i]) + str(train_y3[i]))
    trainList.append(class_dict.get(dataForLine))

train_y = pd.Series(trainList)


train = z_score(trainPreNorm)
test = z_score(testPreNorm)

model = keras.Sequential([
    keras.layers.Dense(200, activation='relu'),  # hidden layer (2)
    keras.layers.Dense(200, activation='relu'),  # hidden layer (2)

    keras.layers.Dense(24, activation='softmax')  # output layer (3)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train, train_y, epochs=2)

test_loss, test_acc = model.evaluate(test,  test_y, verbose=1)

print('Test accuracy:', test_acc)

model.save('kerasModelEveryone')
