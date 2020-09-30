from players import *
import math
import random

def nextPlayer(players, currentPlayer):
    # takes the players in the game and the current player and returns the next one
    index = players.index(currentPlayer)
    if index + 2 <= len(players):
        return players[index+1]
    else:
        return players[0]

class presRound(object):
    def __init__(self, players, startingPlayer):
        self.players = players
        self.currentPlayer = startingPlayer
        self.currentCards = []
        self.prevCards = []
        self.passCounter = 0

    def nextPlayerStart(self):
        self.currentPlayer = nextPlayer(self.players, self.currentPlayer)
        self.currentCards = self.currentPlayer.start()
        self.prevCards = []
        # print(self.currentPlayer.name, "started with ", self.currentCards)

    def nextPlayerPlay(self):
        self.prevCards = self.currentCards
        self.currentPlayer = nextPlayer(self.players, self.currentPlayer)
        self.currentCards = self.currentPlayer.play(self.prevCards)
        # print(self.currentPlayer.name, "played ", self.currentCards)

    def currentPlayerStart(self):
        self.currentCards = self.currentPlayer.start()
        self.prevCards = []
        # print(self.currentPlayer.name, "started with ", self.currentCards)

    def currentPlayerPlay(self):
        self.prevCards = self.currentCards
        self.currentCards = self.currentPlayer.play(self.prevCards)
        # print(self.currentPlayer.name, "played ", self.currentCards)

    def startRound(self):
        # sets up some variables
        playersOutOrder = []

        # starts the play
        self.currentPlayerStart()

        # this while loop only returns once everyone is out
        while len(self.players) > 0:

            # start of if statements to determine what card was just played

            # if someone passes
            if self.currentCards[0] == 'pass':
                self.passCounter += 1
                # if everyone has passed
                if self.passCounter == len(self.players) - 1:
                    # print("everyone passed")
                    self.nextPlayerStart()
                    continue
                # if not everyone has passed
                else:
                    self.currentCards = self.prevCards
                    self.nextPlayerPlay()
                    continue

            # if a match happened or a two was played
            elif self.currentCards == self.prevCards or self.currentCards[0] == 2:
                # print('match or two')
                self.currentPlayerStart()
                continue

            # if the player is out
            elif self.currentCards[0] == 'out':
                # print(self.currentPlayer.name, " went out -------------------------------")
                # puts them on the list
                playersOutOrder.append(self.currentPlayer)
                playerToBeRemoved = self.currentPlayer
                # switches to the next player
                self.currentPlayer = nextPlayer(self.players, self.currentPlayer)
                # removes them from players
                self.players.remove(playerToBeRemoved)

                # checks if everyone is out (minus the last person)
                if len(self.players) == 1:
                    playersOutOrder.append(self.currentPlayer)
                    break

                # checks if someone started with out
                if self.prevCards == []:
                    # if they did then next person starts (already swapped person)
                    self.currentPlayerStart()
                    continue

                # if they didn't then next person plays (already swapped person)
                # if everyone has passed (bc amount of people just changed)
                elif self.passCounter == len(self.players) - 1:
                    # print("everyone passed")
                    self.currentPlayerStart()
                    continue
                # if not everyone passed then next person plays
                else:
                    self.currentCards = self.prevCards
                    self.currentPlayerPlay()
                    continue

            # if it gets to here then they just played something not special
            else:
                # print("nothing extraordinary happened")
                self.passCounter = 0
                self.nextPlayerPlay()

        return playersOutOrder