import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

model = keras.models.load_model('kerasModel')

for i in range(400):
    hand = []
    hand.append(int(input("Starting player? (0 or 1): ")))
    for i in range(2, 15):
        hand.append(int(input("How many " + str(i) + "s? ")))

    predictions = model.predict([hand])
    print(predictions[0])
    print(np.argmax(predictions[0]))