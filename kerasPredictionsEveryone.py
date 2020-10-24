import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

class_dict = {  0:'0123',
                1:'0132',
                2:'0231',
                3:'0213',
                4:'0312',
                5:'0321',
                6:'1023',
                7:'1032',
                8:'1230',
                9:'1203',
                10:'1302',
                11:'1320',
                12:'2103',
                13:'2130',
                14:'2031',
                15:'2013',
                16:'2310',
                17:'2301',
                18:'3120',
                19:'3102',
                20:'3201',
                21:'3210',
                22:'3012',
                23:'3021'
}

model = keras.models.load_model('kerasModelEveryone')

def makePrediction():
    hand = []
    for i in range(0,4):
        starting = int(input("Starting player? (0 or 1): "))
        if starting == 1:
            hand.append(1.7)
        elif starting == 0:
            hand.append(-0.5)
        inputHand = (str(input("Please input the hand: ")))
        handDict = {}
        for num in inputHand.split(inputHand[1]):
            if num not in handDict.keys():
                handDict[num] = 1
            else:
                handDict[num] += 1
        for num in range(2,15):
            amount = handDict.get(str(num), 0)
            if amount == 0:
                hand.append(-1.5)
            elif amount == 1:
                hand.append(0.0)
            elif amount == 2:
                hand.append(1.2)
            elif amount == 3:
                hand.append(2.4)
            elif amount == 4:
                hand.append(3.5)

    predictions = model.predict([hand])
    print(class_dict.get(np.argmax(predictions[0])))
    return class_dict.get(np.argmax(predictions[0]))

for i in range(400):
    makePrediction()