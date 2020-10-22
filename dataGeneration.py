from player import *
from game import *
import pandas as pd

game13 = Game(4, 'game1', 10000, 'none', 1, Player, False, Player, 0, True, None, True)
game13.startGame()
data = pd.DataFrame(game13.getData(), columns=["role", "isStarting", 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
# print(data)
data.to_csv('evalData.csv')