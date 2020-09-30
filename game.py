from players import *
from decks_and_cards import *
from presRound import *
import math
import random


class Game(object):
    def __init__(self, numberOfPlayers, name, numRounds, print):
        self.name = name
        self.deck = False
        self.players = []
        self.numberOfPlayers = numberOfPlayers
        self.dealHands()
        self.numRounds = numRounds
        self.playersOutOrder = []
        self.startingPlayer = False
        # makes players
        for i in range(self.numberOfPlayers):
            self.players.append(Player(i))
        self.dealHands()
        self.print = print

    def dealHands(self):
        # makes and shuffles new deck
        self.deck = Deck()
        self.deck.shuffle()
        # gives players their hands
        for player in self.players:
            player.resetPlayer()
            player.draw(self.deck, 13)
            player.sortHand()

    def startGame(self):
        # checks who has the four of clubs and sets them to be starting player
        for player in self.players:
            for card in player.showHand():
                if card.value == 4 and card.suit == 'Clubs':
                    self.startingPlayer = player
                    print('starting player:', self.startingPlayer.name)
                    break

        # heuristic stuff
        numberofTimesAssStayed = 0
        numberofTimesPresStayed = 0
        numberofTimesVPStayed = 0
        numberofTimesVAStayed = 0

        # plays the given amount of rounds
        for i in range(self.numRounds):

            # heuristic stuff
            ass = self.players[3]
            pres = self.players[0]
            vp = self.players[1]
            va = self.players[2]

            # starts the playing of rounds
            newRound = presRound(self.players, self.startingPlayer, self.print)
            self.playersOutOrder = newRound.startRound()
            for player in self.playersOutOrder:
                print(player.name)
            print("---------------------------")

            # heuristic stuff
            if ass == self.playersOutOrder[3]:
                numberofTimesAssStayed += 1
            if pres == self.playersOutOrder[0]:
                numberofTimesPresStayed += 1
            if vp == self.playersOutOrder[1]:
                numberofTimesVPStayed += 1
            if va == self.playersOutOrder[2]:
                numberofTimesVAStayed += 1

            self.players = self.playersOutOrder
            self.dealHands()
            self.doTopTwoCardsForFourPlayers()

        print(numberofTimesPresStayed/self.numRounds, " prez stayed")
        print(numberofTimesVPStayed/self.numRounds, " vp stayed")
        print(numberofTimesVAStayed/self.numRounds, " va stayed")
        print(numberofTimesAssStayed/self.numRounds, " ass stayed")

    def doTopOneCardForFourPlayers(self):
        # gets cards
        self.startingPlayer = self.playersOutOrder[0]
        bestOneA = self.playersOutOrder[3].giveHighestCard()
        worstOneP = self.playersOutOrder[0].giveLowestCard()
        worstOneVA = self.playersOutOrder[2].giveLowestCard()
        self.playersOutOrder[1].cardDict[worstOneVA] += 1
        worstOneVP = self.playersOutOrder[1].giveLowestCard()
        self.playersOutOrder[0].cardDict[bestOneA] += 1
        self.playersOutOrder[2].cardDict[worstOneVP] += 1
        self.playersOutOrder[3].cardDict[worstOneP] += 1

    def doTopTwoCardsForFourPlayers(self):
        bestTwo = []
        worstTwo = []
        worstOne = []
        bestOne = []

        # gets cards
        for player in self.players:
            if self.playersOutOrder.index(player) == 0:
                self.startingPlayer = player
                worstTwo.append(player.giveLowestCard())
                worstTwo.append(player.giveLowestCard())
            elif self.playersOutOrder.index(player) == 1:
                worstOne.append(player.giveLowestCard())
            elif self.playersOutOrder.index(player) == 2:
                bestOne.append(player.giveHighestCard())
            elif self.playersOutOrder.index(player) == 3:
                bestTwo.append(player.giveHighestCard())
                bestTwo.append(player.giveHighestCard())

        # gives cards
        for player in self.playersOutOrder:
            if self.playersOutOrder.index(player) == 0:
                for card in bestTwo:
                    player.cardDict[card] += 1
            elif self.playersOutOrder.index(player) == 1:
                for card in bestOne:
                    player.cardDict[card] += 1
            elif self.playersOutOrder.index(player) == 2:
                for card in worstOne:
                    player.cardDict[card] += 1
            elif self.playersOutOrder.index(player) == 3:
                for card in worstTwo:
                    player.cardDict[card] += 1


# script
game1 = Game(4, 1, 50000, False)
game1.startGame()
