import math
import random

values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

class Player(object):
    # this is the default player object that all other players are built off of (currently performs the best)
    # this object handles playing cards, starting tricks as well as keeping track of its own hand
    def __init__(self, name):
        self.name = name
        self.startingHand = []
        self.valHand = []
        # this dictionary is the thing that the player uses 99% of the time, it will be populated with how many of each card the player has
        self.cardDict = {
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0
        }
        self.totalCards = 0

    def resetPlayer(self):
        # when a new round starts this is called to reset the players hand (bc/ the same objects are reused across rounds)
        self.startingHand = []
        self.valHand = []
        self.cardDict = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        self.totalCards = 0

    def sortHand(self):
        # sorts the players hand into a readable hand for us (valHand) and a dictionary for use by the player object
        for card in self.startingHand:
            self.valHand.append(card.value)
        self.valHand.sort()

        # fills in dictionary for how many of each card they have
        for card in self.valHand:
            self.totalCards += 1
            for typeOfCard in self.cardDict:
                if card == typeOfCard:
                    self.cardDict[typeOfCard] += 1
        # print(self.cardDict)

    def draw(self, deck, num=1):
        # draw n number of cards from a given deck
        for i in range(num):
            self.startingHand.append(deck.draw())

    def showValHand(self):
        return self.valHand

    def showHand(self):
        return self.startingHand

    def checkIfAnyNegatives(self):
        # just a testing function to see if they have any cards that they have a negative amount of
        for card in self.cardDict:
            if self.cardDict[card] < 0:
                print(self.name, "has negative cards")
                print(self.cardDict)

    def play(self, cardsOnTop):

        # print(self.name,"'s hand: ",self.cardDict)

        # checks if they are out
        self.totalCards = 0
        for card in self.cardDict:
            self.totalCards += self.cardDict[card]
        if self.totalCards == 0:
            return ['out']

        # checks if they only have twos and one other trick
        if self.checkIfGuaranteedOut():
            self.cardDict[2] -= 1
            return [2, 1]

        # loops through cardDict (goes forward so plays lowest possible first)
        for card in self.cardDict:
            # checks if its the same type of trick and if they have enough cards to play on the trick (at least one)
            if self.cardDict[card] + self.cardDict[3] >= cardsOnTop[1] and self.cardDict[card] > 0:
                # checks if the card is playable and not a two or three
                # (shouldn't be possible to be a two or three cuz it should be a four or higher)
                if card >= cardsOnTop[0] and not card == 2 and not card == 3:
                    # checks to see if you have enough of the card to play without threes (won't break up larger sets)
                    if self.cardDict[card] - cardsOnTop[1] == 0:
                        self.cardDict[card] -= cardsOnTop[1]
                        return [card, cardsOnTop[1]]
                    # this says it is ok to break up larger pairs if it is for matching or if its a high card
                    elif self.cardDict[card] - cardsOnTop[1] > 0 and (card == cardsOnTop[0] or card >= 10):
                        # note -- the value 10 in the if statement above was determined by testing different values through many millions of games
                        self.cardDict[card] -= cardsOnTop[1]
                        return [card, cardsOnTop[1]]
                    # if you don't have enough without threes, plays what you do have as well as threes, but not if its matching
                    elif card != cardsOnTop[0] and cardsOnTop[1] > 1 and self.cardDict[card] < cardsOnTop[1]:
                        threesUsed = cardsOnTop[1] - self.cardDict[card]
                        self.cardDict[3] -= cardsOnTop[1] - self.cardDict[card]
                        # should always set it to 0
                        self.cardDict[card] -= cardsOnTop[1] - threesUsed
                        self.checkIfAnyNegatives()
                        return [card, cardsOnTop[1], "Threes used:", threesUsed]

        # if it gets to here then it has nothing to play other than 2's and 3's

        # checks if it has 2's to play
        if self.cardDict[2] > 0:
            self.cardDict[2] -= 1
            return [2, 1]
        # checks if it has enough 3's to play as aces
        if cardsOnTop[0] < 14 and self.cardDict[3] >= cardsOnTop[1]:
            self.cardDict[3] -= cardsOnTop[1]
            return [14, cardsOnTop[1], "Threes used:", cardsOnTop[1]]

        # if it has not returned by now then it needs to pass
        return ['pass']

    def start(self):

        # checks if they are out
        self.totalCards = 0
        for card in self.cardDict:
            self.totalCards += self.cardDict[card]
        if self.totalCards == 0:
            return ['out']

        # checks if you only have twos and one other trick
        if self.checkIfGuaranteedOut():
            self.cardDict[2] -= 1
            return [2, 1]

        # checks if only one trick is left (counting threes) and then plays that trick with all the threes
        if self.onlyOneTrick():
            for card in self.cardDict:
                if card != 3 and self.cardDict[card] > 0:
                    amountOfCard = self.cardDict[card] + self.cardDict[3]
                    threesUsed = self.cardDict[3]
                    self.cardDict[card] = 0
                    self.cardDict[3] = 0
                    if threesUsed > 0: return [card, amountOfCard, "Threes used:", threesUsed]
                    else: return [card, amountOfCard]

        # loops through card forward
        for card in self.cardDict:
            # checks the first card that isn't a two or three and plays all of it
            if card != 2 and card != 3 and self.cardDict[card] > 0:
                amountOfCard = self.cardDict[card]
                self.cardDict[card] -= self.cardDict[card]
                return [card, amountOfCard]

        # if it gets to here then it only has twos and threes
        # first checks and plays twos
        if self.cardDict[2] > 0:
            self.cardDict[2] -= 1
            return [2, 1]
        # then checks and plays threes
        elif self.cardDict[3] > 0:
            amountOfCard = self.cardDict[3]
            self.cardDict[3] = 0
            return [14, amountOfCard, "Threes used:", amountOfCard]

        print(self.name + "Error: start() didn't return?")

    def checkIfGuaranteedOut(self):
        # check if the person can go out guaranteed by playing a two
        if self.onlyOneTrick() and self.cardDict[2] > 0:
            return True
        else:
            return False

    def onlyOneTrick(self):
        # checks if the person has only one type of trick left
        numberOfTricks = 0
        for card in self.cardDict:
            if card != 2 and card != 3 and self.cardDict[card] > 0:
                numberOfTricks += 1
        if numberOfTricks == 1:
            return True
        else:
            return False

    def giveLowestCard(self):
        # removes and returns the lowest card the players hand
        for card in self.cardDict:
            if card != 2 and card != 3 and self.cardDict[card] > 0:
                self.cardDict[card] -= 1
                return card

    def giveHighestCard(self):
        # removes and returns the highest card in the players hand
        # checks for twos
        if self.cardDict[2] > 0:
            self.cardDict[2] -= 1
            return 2
        # checks for threes
        if self.cardDict[3] > 0:
            self.cardDict[3] -= 1
            return 3
        # loops through dict to find next highest card
        # cant loop through dict reversed so i made a list of the cards (keys for the dict) at the top of this file
        for card in reversed(values):
            if self.cardDict[card] > 0:
                self.cardDict[card] -= 1
                return card
