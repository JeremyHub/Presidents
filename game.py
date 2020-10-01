from player import *
from decks_and_cards import *
from presRound import *
from badPlayer import *
from randomPlayer import *
from worstPlayer import *
from noTwoPlayer import *
from twoerPlayer import *
from personInputPlayer import *
import math
import random


class Game(object):
    def __init__(self, numberOfPlayers, name, numRounds, passingRules, numDecks, newPlayer, restOfPlayers):
        self.name = name
        self.deck = False
        self.players = []
        self.numberOfPlayers = numberOfPlayers
        self.numRounds = numRounds
        self.playersOutOrder = []
        self.startingPlayer = False
        self.passingRules = passingRules
        self.numDecks = numDecks
        self.newPlayer = newPlayer

        # makes players
        for i in range(self.numberOfPlayers - 1):
            self.players.append(restOfPlayers(i))
        self.players.append(self.newPlayer)

        self.dealHands()

    def dealHands(self):
        # makes and shuffles new deck
        self.deck = Deck(self.numDecks)
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
                    # print('starting player:', self.startingPlayer.name)
                    break

        # heuristic stuff
        numberofTimesAssToPres = 0
        numberofTimesPresToPres = 0
        numberofTimesVPToPres = 0
        numberofTimesVAToPres = 0
        numberofTimesNewPlayerPres = 0

        # plays the given amount of rounds
        for i in range(self.numRounds):

            # heuristic stuff
            ass = self.players[self.numberOfPlayers - 1]
            pres = self.players[0]
            vp = self.players[1]
            va = self.players[self.numberOfPlayers - 2]

            # starts the playing of rounds
            newRound = presRound(self.players, self.startingPlayer)
            self.playersOutOrder = newRound.startRound()
            # for player in self.playersOutOrder:
            #     print(player.name)
            # print("---------------------------")

            # heuristic stuff
            if ass == self.playersOutOrder[0]:
                numberofTimesAssToPres += 1
            if pres == self.playersOutOrder[0]:
                numberofTimesPresToPres += 1
            if vp == self.playersOutOrder[0]:
                numberofTimesVPToPres += 1
            if va == self.playersOutOrder[0]:
                numberofTimesVAToPres += 1
            if pres == self.newPlayer:
                numberofTimesNewPlayerPres += 1

            self.players = self.playersOutOrder
            self.dealHands()
            if self.passingRules == 'two':
                self.doTopTwoCards()
            elif self.passingRules == 'one':
                self.doTopOneCard()
            elif self.passingRules == 'hybrid':
                self.doHybridPassing()

        print(numberofTimesPresToPres/self.numRounds, " prez went to p")
        print(numberofTimesVPToPres/self.numRounds, " vp went to p")
        print(numberofTimesVAToPres/self.numRounds, " va went to p")
        print(numberofTimesAssToPres/self.numRounds, " ass went to p")
        # print(numberofTimesNewPlayerPres/self.numRounds, "% games other player was pres")

    def doHybridPassing(self):
        bestTwo = []
        worstTwo = []
        # gets cards
        for player in self.players:
            if self.playersOutOrder.index(player) == 0:
                self.startingPlayer = player
                worstTwo.append(player.giveLowestCard())
                worstTwo.append(player.giveLowestCard())
            elif self.playersOutOrder.index(player) == self.numberOfPlayers - 1:
                bestTwo.append(player.giveHighestCard())
                bestTwo.append(player.giveHighestCard())

        # gives cards
        for player in self.playersOutOrder:
            if self.playersOutOrder.index(player) == 0:
                for card in bestTwo:
                    player.cardDict[card] += 1
            elif self.playersOutOrder.index(player) == self.numberOfPlayers - 1:
                for card in worstTwo:
                    player.cardDict[card] += 1

        # does va/vp passing
        worstOneVA = self.playersOutOrder[self.numberOfPlayers - 2].giveLowestCard()
        self.playersOutOrder[1].cardDict[worstOneVA] += 1
        worstOneVP = self.playersOutOrder[1].giveLowestCard()
        self.playersOutOrder[self.numberOfPlayers - 2].cardDict[worstOneVP] += 1

    def doTopOneCard(self):
        # gets cards and gives cards
        self.startingPlayer = self.playersOutOrder[0]
        bestOneA = self.playersOutOrder[self.numberOfPlayers - 1].giveHighestCard()
        worstOneP = self.playersOutOrder[0].giveLowestCard()
        worstOneVA = self.playersOutOrder[self.numberOfPlayers - 2].giveLowestCard()
        self.playersOutOrder[1].cardDict[worstOneVA] += 1
        worstOneVP = self.playersOutOrder[1].giveLowestCard()
        self.playersOutOrder[0].cardDict[bestOneA] += 1
        self.playersOutOrder[self.numberOfPlayers - 2].cardDict[worstOneVP] += 1
        self.playersOutOrder[self.numberOfPlayers - 1].cardDict[worstOneP] += 1

    def doTopTwoCards(self):
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
            elif self.playersOutOrder.index(player) == self.numberOfPlayers - 2:
                bestOne.append(player.giveHighestCard())
            elif self.playersOutOrder.index(player) == self.numberOfPlayers - 1:
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
            elif self.playersOutOrder.index(player) == self.numberOfPlayers - 2:
                for card in worstOne:
                    player.cardDict[card] += 1
            elif self.playersOutOrder.index(player) == self.numberOfPlayers - 1:
                for card in worstTwo:
                    player.cardDict[card] += 1