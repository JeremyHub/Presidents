import numpy as np
import pandas as pd

CSV_COLUMN_NAMES = ["role", 'isStarting', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
ROLES = ['pres', 'vp', 'va', 'ass']

newColumns = ['role0', 'isStarting0', '2(0)', '3(0)', '4(0)', '5(0)', '6(0)', '7(0)', '8(0)', '9(0)', '10(0)', '11(0)', '12(0)', '13(0)', '14(0)',
            'role1', 'isStarting1', '2(1)', '3(1)', '4(1)', '5(1)', '6(1)', '7(1)', '8(1)', '9(1)', '10(1)', '11(1)', '12(1)', '13(1)', '14(1)',
            'role2', 'isStarting2', '2(2)', '3(2)', '4(2)', '5(2)', '6(2)', '7(2)', '8(2)', '9(2)', '10(2)', '11(2)', '12(2)', '13(2)', '14(2)',
            'role3', 'isStarting3', '2(3)', '3(3)', '4(3)', '5(3)', '6(3)', '7(3)', '8(3)', '9(3)', '10(3)', '11(3)', '12(3)', '13(3)', '14(3)']

# train_path = open('everyoneTrainData.csv')
test_path = open('everyoneEvalData.csv')

# train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
test = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)

# train_y = train.pop('role')
test_y = test.pop('role')

everyone = []
count = 0
currentGame = []
for index, row in test.iterrows():
    if count < 4:
        currentGame.append(row)
        count += 1
    else:
        count = 0
        everyone.append(currentGame)
        currentGame = []

everyoneDf = pd.DataFrame(everyone, index=newColumns, columns=index)
print(everyoneDf)