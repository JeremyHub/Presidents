import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

model = keras.models.load_model('kerasModel')
# model = keras.models.load_model('kerasModelUpperLower')

def makePrediction():
    hand = []
    starting = int(input("Starting player? (0 or 1): "))
    if starting == 1:
        hand.append(1.7)
    elif starting == 0:
        hand.append(-0.5)
    inputHand = (str(input("Please input the hand: ")))
    handDict = {}
    for num in inputHand.split(inputHand[1]):
        if not num in handDict.keys():
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
    print(predictions[0])
    print(np.argmax(predictions[0]))
    return np.argmax(predictions[0])

for i in range(400):
    makePrediction()