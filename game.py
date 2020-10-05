from player import *
from decks_and_cards import *
from presRound import *
from randomPlayer import *
from worstPlayer import *
from noTwoPlayer import *
from twoerPlayer import *
from personInputPlayer import *
import math
import random


class Game(object):
    # this object is the only thing that the player interacts with, it manages the playing of rounds and the creation of players,
    # it also manages the exchanges of cards before the round starts and different heuristics I was curious about
    def __init__(self, numberOfPlayers, name, numRounds, passingRules, numDecks, restOfPlayers, print=False, newPlayer=Player, amountOfNewPlayers=0):
        self.name = name
        self.deck = False
        self.players = []
        self.numberOfPlayers = numberOfPlayers
        self.numRounds = numRounds
        self.playersOutOrder = []
        self.startingPlayer = False
        self.passingRules = passingRules
        self.numDecks = numDecks
        self.lastPlayer = newPlayer
        self.amountOfNewPlayers = amountOfNewPlayers
        self.print = print

        # makes players
        for i in range(self.numberOfPlayers - self.amountOfNewPlayers):
            self.players.append(restOfPlayers(i))
        for i in range(self.amountOfNewPlayers):
            self.players.append(self.lastPlayer(i + self.numberOfPlayers - self.amountOfNewPlayers))
            self.lastPlayer = self.players[self.numberOfPlayers - 1]


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

        # heuristic variable setup
        numberofTimesAssToPres = 0
        numberofTimesPresToPres = 0
        numberofTimesVPToPres = 0
        numberofTimesVAToPres = 0
        numberofTimesNewPlayerPres = 0

        # plays the given amount of rounds
        for i in range(self.numRounds):
            # prints a progress bar
            if not self.print: print(f'\r{"Percent Complete: "} {math.ceil((i/self.numRounds)*100)}% ', end='')
            # heuristic role assignment
            ass = self.players[self.numberOfPlayers - 1]
            pres = self.players[0]
            vp = self.players[1]
            va = self.players[self.numberOfPlayers - 2]

            # starts the playing of rounds (this plays one round, the for loop above plays more rounds)
            newRound = presRound(self.players, self.startingPlayer, self.print)
            self.playersOutOrder = newRound.startRound()
            printablePlayersOutOrder = []
            for player in self.playersOutOrder:
                printablePlayersOutOrder.append(player.name)
            # print("The below shows the players in order of when they went out.")
            # print(printablePlayersOutOrder)
            # print("---------------------------")

            # heuristic role checking
            if ass == self.playersOutOrder[0]:
                numberofTimesAssToPres += 1
            if pres == self.playersOutOrder[0]:
                numberofTimesPresToPres += 1
            if vp == self.playersOutOrder[0]:
                numberofTimesVPToPres += 1
            if va == self.playersOutOrder[0]:
                numberofTimesVAToPres += 1
            if pres == self.lastPlayer:
                numberofTimesNewPlayerPres += -2
            elif vp == self.lastPlayer:
                numberofTimesNewPlayerPres += -1
            elif va == self.lastPlayer:
                numberofTimesNewPlayerPres += 1
            elif ass == self.lastPlayer:
                numberofTimesNewPlayerPres += 2

            # checks what passing rules the game is operating under and implements that
            self.players = self.playersOutOrder
            self.dealHands()
            if self.passingRules == 'two':
                self.doTopTwoCards()
            elif self.passingRules == 'one':
                self.doTopOneCard()
            elif self.passingRules == 'hybrid':
                self.doHybridPassing()

        # prints heuristic data
        if not self.print: print("\n")
        print(round((numberofTimesPresToPres/self.numRounds)*100,4), "% prez went to p")
        print(round((numberofTimesVPToPres/self.numRounds)*100,4), "% vp went to p")
        print(round((numberofTimesVAToPres/self.numRounds)*100,4), "% va went to p")
        print(round((numberofTimesAssToPres/self.numRounds)*100,4), "% ass went to p")
        if (self.amountOfNewPlayers > 0):
            print(numberofTimesNewPlayerPres/self.numRounds, " average score (higher is worse, avg is 0) of the last player")

    def doHybridPassing(self):
        # one of the passing rules, this is a hybrid of the two passing rules (functions) below this one
        # this was setup to see how powerful pres would be if vp was in its weakest form and p was in its strongest
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
        # a passes best to p, p passes worst to a, va passes worst to vp, vp passes worst to va
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
        # a passes best two to p, p worst two to a, va best one to vp, vp worst one to va
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