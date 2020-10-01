import math
import random

values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

class Player(object):
    def __init__(self, name):
        self.name = name
        self.startingHand = []
        self.valHand = []
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
        self.startingHand = []
        self.valHand = []
        self.cardDict = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        self.totalCards = 0

    def sortHand(self):
        for card in self.startingHand:
            self.valHand.append(card.value)
        self.valHand.sort()

        # makes dictionary for how many of each card they have
        for card in self.valHand:
            self.totalCards += 1
            for typeOfCard in self.cardDict:
                if card == typeOfCard:
                    self.cardDict[typeOfCard] += 1

        # print(self.cardDict)

    # Draw n number of cards from a given deck
    def draw(self, deck, num=1):
        for i in range(num):
            self.startingHand.append(deck.draw())

    def showValHand(self):
        return self.valHand

    def showHand(self):
        return self.startingHand

    def play(self, cardsOnTop):

        # checks if they are out
        self.totalCards = 0
        for card in self.cardDict:
            self.totalCards += self.cardDict[card]
        if self.totalCards == 0:
            return ['out']

        # checks if only twos and something else
        if self.checkIfOnlyTwos():
            self.cardDict[2] -= 1
            return [2, 1]

        # loops through cardDict (goes forward so should play lowest first)
        for card in self.cardDict:
            # checks if its the same type of trick and if they have enough cards to play on the trick (at least one)
            if self.cardDict[card] + self.cardDict[3] >= cardsOnTop[1] and self.cardDict[card] > 0:
                # checks if the card is playable and not a two or three
                # (shouldn't be possible to be a two or three cuz it should be a four or higher)
                if card >= cardsOnTop[0] and not card == 2 and not card == 3:
                    # checks to see if you have enough of the card to play without threes
                    if self.cardDict[card] - cardsOnTop[1] >= 0:
                        self.cardDict[card] -= cardsOnTop[1]
                        return [card, cardsOnTop[1]]
                    # if you don't have enough without threes, plays what you do have as well as threes, but not if its matching
                    elif card != cardsOnTop[0]:
                        self.cardDict[3] -= cardsOnTop[1] - self.cardDict[card]
                        self.cardDict[card] = 0
                        return [card, cardsOnTop[1]]

        # if it gets to here then it has nothing to play other than 2's and 3's
        # checks if it has enough 3's to play as aces
        if cardsOnTop[0] < 14 and self.cardDict[3] >= cardsOnTop[1]:
            self.cardDict[3] -= cardsOnTop[1]
            return [14, cardsOnTop[1]]
        # checks if it has 2's to play and plays it
        elif self.cardDict[2] > 0:
            self.cardDict[2] -= 1
            return [2, 1]
        # if it has not returned by now then it needs to pass
        else:
            return ['pass']

    def start(self):

        # checks if they are out
        self.totalCards = 0
        for card in self.cardDict:
            self.totalCards += self.cardDict[card]
        if self.totalCards == 0:
            return ['out']

        # checks if only twos and something else
        if self.checkIfOnlyTwos():
            self.cardDict[2] -= 1
            return [2, 1]

        # loops through card forward
        for card in self.cardDict:
            # checks the first card that isn't a two or three and plays all of it
            if card != 2 and card != 3 and self.cardDict[card] > 0:
                amountOfCard = self.cardDict[card]
                self.cardDict[card] -= self.cardDict[card]
                return [card, amountOfCard]

        # if it gets to here then it only has twos and threes
        # first checks if it has twos to play
        if self.cardDict[2] > 0:
            self.cardDict[2] -= 1
            return [2, 1]
        # then checks and plays threes
        elif self.cardDict[3] > 0:
            amountOfCard = self.cardDict[3]
            self.cardDict[3] = 0
            return [14, amountOfCard]

        print(self.name + "ERROR start() didn't return?")

    def checkIfOnlyTwos(self):
        numberOfDiffCards = 0
        # checks if have twos
        if self.cardDict[2] == 0:
            return False
        # checks how many tricks you have
        for card in self.cardDict:
            if card != 2 and self.cardDict[card] > 0:
                numberOfDiffCards += 1
        # if you have just one trick (other than twos) returns true
        if numberOfDiffCards == 1:
            return True
        else:
            return False

    def giveLowestCard(self):
        for card in self.cardDict:
            if card != 2 and card != 3 and self.cardDict[card] > 0:
                self.cardDict[card] -= 1
                return card

    def giveHighestCard(self):
        if self.cardDict[2] > 0:
            self.cardDict[2] -= 1
            return 2
        if self.cardDict[3] > 0:
            self.cardDict[3] -= 1
            return 3
        # cant loop through dict reversed so i made a list of the cards at the top of this
        for card in reversed(values):
            if self.cardDict[card] > 0:
                self.cardDict[card] -= 1
                return card
