import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

model = keras.models.load_model('kerasModel')

for i in range(400):
    hand = []
    starting = int(input("Starting player? (0 or 1): "))
    if starting == 1:
        hand.append(1.7)
    elif starting == 0:
        hand.append(-0.5)
    for i in range(2, 15):
        num = (int(input("How many " + str(i) + "s? ")))
        if num == 0:
            hand.append(-1.5)
        elif num == 1:
            hand.append(0.0)
        elif num == 2:
            hand.append(1.2)
        elif num == 3:
            hand.append(2.4)
        elif num == 4:
            hand.append(3.5)

    predictions = model.predict([hand])
    print(predictions[0])
    print(np.argmax(predictions[0]))