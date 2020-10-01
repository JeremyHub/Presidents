from player import *
from game import *
from decks_and_cards import *
from presRound import *
from badPlayer import *
from randomPlayer import *
from worstPlayer import *
from noTwoPlayer import *
from twoerPlayer import *
from personInputPlayer import *

# script
print("-----------------------")

game1 = Game(4, 'game1', 10, 'two', 1, PlayerInputPlayer(3))
game1.startGame()

# print("-----------------------below is passing one")
#
# game1 = Game(4, 'game2', 10000, 'one', 1, Player(3))
# game1.startGame()
#
# print("-----------------------below is passing two but vp/va doing the trade thing")
#
# game1 = Game(4, 'game2', 10000, 'hybrid', 1, Player(3))
# game1.startGame()