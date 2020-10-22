from player import *
from decks_and_cards import *
from presRound import *
import math
import random
import pandas as pd


class Game(object):
    # this object is the only thing that the player interacts with, it manages the playing of rounds and the creation of players,
    # it also manages the exchanges of cards before the round starts and different heuristics I was curious about
    def __init__(self, numberOfPlayers, name, numRounds, passingRules, numDecks, restOfPlayers, print=False, newPlayer=Player, amountOfNewPlayers=1, anti=False, test=None, generateData=False):
        '''
        :param numberOfPlayers: the number of players in the game
        :param name: the name of the game
        :param numRounds: the number of rounds the game should go through
        :param passingRules: the passing rules the game should operate under
        :param numDecks: number of decks used
        :param restOfPlayers: which of the player objects should comprise the game
        :param print: True: prints out every single card every bot plays
                      False: after all games are done, prints out statistics on the games
        :param newPlayer: second type of player object (default is normal Player)
        :param amountOfNewPlayers: number of players of the type above (default 1)
        :param anti: should there be an anti in this game?
        :param test: just for passing random things that I want to test to other objects
        :param generateData: should the program put the data from the games into a file?
        '''
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
        self.anti = anti
        self.test = test
        self.generateData = generateData
        self.data = []

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

    def getData(self):
        return self.data

    def startGame(self):
        # checks who has the four of clubs and sets them to be starting player
        for player in self.players:
            for card in player.showHand():
                if card.value == 4 and card.suit == 'Clubs':
                    self.startingPlayer = player
                    if self.print: print('starting player:', self.startingPlayer.name)
                    break

        # heuristic variable setup
        numberofTimesAssToPres = 0
        numberofTimesPresToPres = 0
        numberofTimesVPToPres = 0
        numberofTimesVAToPres = 0
        numberofTimesNewPlayerPres = 0

        isFirstRound = True

        # plays the given amount of rounds
        for i in range(self.numRounds):
            # prints a progress bar
            if not self.print: print(f'\r{"Percent Complete: "} {math.ceil((i/self.numRounds)*100)}% ', end='')

            # heuristic role assignment
            ass = self.players[self.numberOfPlayers - 1]
            pres = self.players[0]
            vp = self.players[1]
            va = self.players[self.numberOfPlayers - 2]

            # generates some data about the player's hands for use later
            cardsForPlayers = []
            if self.generateData:
                # loops through players
                for player in self.players:
                    playerData = []
                    # appends the player (this will be deleted later)
                    playerData.append(player)
                    # appends if they were the starting player
                    if player is self.startingPlayer:
                        playerData.append(1)
                    else:
                        playerData.append(0)
                    # puts cards in the list
                    for card in player.cardDict:
                        playerData.append(player.cardDict[card])
                    cardsForPlayers.append(playerData)

            # does the anti
            if self.anti:
                self.doAnti()

            # starts the playing of rounds (this plays one round, the for loop above plays more rounds)
            newRound = presRound(self.players, self.startingPlayer, self.print)
            self.playersOutOrder = newRound.startRound()
            if self.print:
                printablePlayersOutOrder = []
                for player in self.playersOutOrder:
                    printablePlayersOutOrder.append(player.name)
                print("The below shows the players in order of when they went out.")
                print(printablePlayersOutOrder)
                print("---------------------------")

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
                numberofTimesNewPlayerPres += 2
            elif vp == self.lastPlayer:
                numberofTimesNewPlayerPres += 1
            elif va == self.lastPlayer:
                numberofTimesNewPlayerPres += -1
            elif ass == self.lastPlayer:
                numberofTimesNewPlayerPres += -2

            # sets players to the new playersOutOrder
            self.players = self.playersOutOrder

            # generates data for use
            for playerDat in cardsForPlayers:
                for player in self.players:
                    if playerDat[0] is player:
                        playerDat.pop(0)
                        playerDat = [self.players.index(player)] + playerDat
                        self.data.append(playerDat)

            # deals hands
            self.dealHands()

            # checks passing rules and implements them
            if self.passingRules == 'two':
                self.doTopTwoCards()
            elif self.passingRules == 'one':
                self.doTopOneCard()
            elif self.passingRules == 'hybrid':
                self.doHybridPassing()
            elif self.passingRules == 'none':
                pass
            self.players = self.playersOutOrder

        # prints heuristic data
        if not self.print:
            print("\n")
            print(round((numberofTimesPresToPres/self.numRounds)*100,4), "% prez went to p")
            print(round((numberofTimesVPToPres/self.numRounds)*100,4), "% vp went to p")
            print(round((numberofTimesVAToPres/self.numRounds)*100,4), "% va went to p")
            print(round((numberofTimesAssToPres/self.numRounds)*100,4), "% ass went to p")
            if (self.amountOfNewPlayers > 0):
                print(numberofTimesNewPlayerPres/self.numRounds, " average score (higher is better, avg is 0) of the last player")

    def doAnti(self):
        cardsInAnti = []
        howManyCardsPerPlayer = {}
        # loops through all players and adds their cards to the anti
        for player in self.players:
            cards = player.anti()
            cardsInAnti += cards
            howManyCardsPerPlayer[player.name] = len(cards)
            if self.print:
                print("Player: " + str(player.name) + " put in the following to the anti.")
                print(cards)
        # shuffles anti
        random.shuffle(cardsInAnti)
        # loops through players and gives them their cards
        for player in self.players:
            if self.print: print("" + "Player: " + str(player.name) + " got the following in the anti")
            for i in range(howManyCardsPerPlayer[player.name]):
                card = cardsInAnti.pop()
                player.cardDict[card] += 1
                if self.print: print(str(card), end="")
            if self.print: print("")

    def doHybridPassing(self):
        # one of the passing rules, this is a hybrid of the two passing rules (functions) below this one
        # this was setup to see how powerful pres would be if vp was in its weakest form and p was in its strongest
        bestTwo = []
        worstTwo = []
        # gets cards
        for player in self.playersOutOrder:
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
        if self.print:
            print("Ass gave pres: ", bestOneA)
            print("VA gave VP: ", worstOneVA)
        self.playersOutOrder[1].cardDict[worstOneVA] += 1
        worstOneVP = self.playersOutOrder[1].giveLowestCard()
        if self.print:
            print("VP gave VA: ", worstOneVP)
            print("Pres gave ass: ", worstOneP)
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
        for player in self.playersOutOrder:
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

        if self.print:
            print("Ass gave pres: ", bestTwo)
            print("VA gave VP: ", bestOne)
            print("VP gave VA: ", worstOne)
            print("Pres gave ass: ", worstTwo)

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