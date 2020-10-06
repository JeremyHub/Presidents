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
    # this is the round object, it manages players playing cards and what those cards do (matching, twos, ect.)
    def __init__(self, players, startingPlayer, print):
        self.players = players
        self.currentPlayer = startingPlayer
        self.currentCards = []
        self.prevCards = []
        self.passCounter = 0
        self.print = print

    def nextPlayerStart(self):
        # asks the next player to start
        self.currentPlayer = nextPlayer(self.players, self.currentPlayer)
        self.currentCards = self.currentPlayer.start()
        self.prevCards = []
        if self.print: print(self.currentPlayer.name, "started with ", self.currentCards)

    def nextPlayerPlay(self):
        # asks the next player to play on the current cards
        self.prevCards = self.currentCards
        self.currentPlayer = nextPlayer(self.players, self.currentPlayer)
        self.currentCards = self.currentPlayer.play(self.prevCards)
        if self.print: print(self.currentPlayer.name, "played ", self.currentCards)

    def currentPlayerStart(self):
        # asks the current player to start
        self.currentCards = self.currentPlayer.start()
        self.prevCards = []
        if self.print: print(self.currentPlayer.name, "started with ", self.currentCards)

    def currentPlayerPlay(self):
        # asks the current player to play on the current cards
        self.prevCards = self.currentCards
        self.currentCards = self.currentPlayer.play(self.prevCards)
        if self.print: print(self.currentPlayer.name, "played ", self.currentCards)

    def startRound(self):
        # sets up some variables
        playersOutOrder = []

        # starts the play
        self.currentPlayerStart()

        # this while loop only returns once everyone is out
        while True:
            # this makes a dict of players' hand sizes to then pass to the players in current cards
            playersHandSizes = {}
            for player in self.players:
                playersHandSizes[player.name] = 0
                for card in player.cardDict:
                    playersHandSizes[player.name] += player.cardDict[card]
            self.currentCards.append(playersHandSizes)

            # start of if statements to determine what card was just played

            # if someone passes
            if self.currentCards[0] == 'pass':
                self.passCounter += 1
                # if everyone has passed
                if self.passCounter == len(self.players) - 1:
                    if self.print: print("everyone passed")
                    self.nextPlayerStart()
                    continue
                # if not everyone has passed
                else:
                    self.currentCards = self.prevCards
                    self.nextPlayerPlay()
                    continue

            # if a match happened or a two was played
            elif self.currentCards[:2] == self.prevCards[:2] or self.currentCards[0] == 2:
                # print('match or two')
                self.currentPlayerStart()
                continue

            # if the player is out
            elif self.currentCards[0] == 'out':
                # puts them on the list
                playersOutOrder.append(self.currentPlayer)
                playerToBeRemoved = self.currentPlayer
                # switches to the next player (have to do this now bc the current player will be removed so nextPlayer() won't work
                self.currentPlayer = nextPlayer(self.players, self.currentPlayer)
                # removes them from players
                self.players.remove(playerToBeRemoved)

                # checks if everyone is out (minus the last person)
                if len(self.players) == 1:
                    playersOutOrder.append(self.currentPlayer)
                    return playersOutOrder

                # checks if someone started with out
                if self.prevCards == []:
                    # if they did then next person starts (already swapped person)
                    self.currentPlayerStart()
                    continue

                # checks if everyone has passed (bc amount of people just changed so the normal check won't work)
                elif self.passCounter == len(self.players) - 1:
                    if self.print: print("everyone passed")
                    self.currentPlayerStart()
                    continue
                # if not everyone passed then next person plays
                else:
                    self.currentCards = self.prevCards
                    self.currentPlayerPlay()
                    continue

            # if it gets to here then they just played something not special
            else:
                self.passCounter = 0
                self.nextPlayerPlay()