import math
import random

values = [2,3,4,5,6,7,8,9,10,11,12,13,14]

class RandomPlayer(object):
    # this player shuffles their dict before doing anything, making them play random (but playable) cards
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

    def checkIfAnyNegatives(self):
        # just a testing function to see if they have any cards that they have a negative amount of
        for card in self.cardDict:
            if self.cardDict[card] < 0:
                print(self.name, "has negative cards")
                print(self.cardDict)

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

        # randomize the dict
            keys = list(self.cardDict.keys())
            random.shuffle(keys)
            shuffledDict = {}
            for key in keys:
                shuffledDict.update({key: self.cardDict[key]})
            self.cardDict = shuffledDict

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

        # loops through randomized card dict and plays a card
        for card in self.cardDict:
            if card >= cardsOnTop[0]:
                if self.cardDict[card] >= cardsOnTop[1]:
                    self.cardDict[card] -= cardsOnTop[1]
                    return [card, cardsOnTop[1]]
                if self.cardDict[card] + self.cardDict[3] >= cardsOnTop[1] and card != cardsOnTop[0]:
                    self.cardDict[3] -= cardsOnTop[1] - self.cardDict[card]
                    self.cardDict[card] = 0
                    return [card, cardsOnTop[1]]

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
