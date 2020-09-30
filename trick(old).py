import math
import random
from players import *


def nextPlayer(players, currentPlayer):
    # takes the players in the game and the current player and returns the next one
    num = currentPlayer.name
    if num + 2 > len(players):
        return players[0]
    else:
        return players[num + 1]


class Trick(object):
    # asks the starting player to start and then assigns variables
    def __init__(self, players, startingPlayer, playersInOrder):
        self.currentCard = []
        self.currentPlayer = startingPlayer
        self.players = players
        self.passCounter = 0
        self.topCard = []
        self.playersInOrder = playersInOrder
        # replaced start here with play to test
        self.currentCard = self.currentPlayer.play(self.currentCard)
        print(self.currentCard[0], self.currentPlayer.name)
        self.currentPlayer = nextPlayer(self.players, self.currentPlayer)
        while self.currentCard == 'out':
            # replaced start here with play
            self.currentCard = self.currentPlayer.play(self.currentCard)
            self.currentPlayer = nextPlayer(self.players, self.currentPlayer)

    def startTrick(self):
        # returns three values, the first is whether everyone is out, the second is the starting person, and the third is the list of ppl who r out

        while True:
            # asks current player to play and switches top card
            self.topCard = self.currentCard
            self.currentCard = self.currentPlayer.play(self.topCard)
            print(self.currentCard[0], self.currentPlayer.name)

            # sets position of the person if they are out and switches the top card
            if self.currentCard[0] == 'out':
                self.currentCard[0] = self.topCard[0]
                if self.currentPlayer.name not in self.playersInOrder:
                    self.playersInOrder.append(self.currentPlayer.name)
                    print(self.currentPlayer.name, "This person was put on the out list", self.playersInOrder)
                # checks if everyone is out
                if len(self.playersInOrder) >= len(self.players):
                    # don't need to return the third thing this time cuz diff stuff happens when true is returned
                    return True, self.playersInOrder

            # implements matching by checking if the currentCard is the same as the prev one
            elif self.currentCard[0] == self.topCard[0] or self.currentCard[0] == 2:
                return False, self.currentPlayer, self.playersInOrder

            # if they pass, increase the pass counter and set the top card to last card
            elif self.currentCard[0] == 'pass':
                self.currentCard[0] = self.topCard[0]
                self.passCounter = self.passCounter + 1
                # if everyone as passed this tells the next current person to start
                if self.passCounter >= len(self.players) - (1 + len(self.playersInOrder)):
                    print('everyone passed')
                    return False, nextPlayer(self.players, self.currentPlayer), self.playersInOrder

            # switches to next player
            self.currentPlayer = nextPlayer(self.players, self.currentPlayer)