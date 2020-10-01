import math
import random

values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

class PlayerInputPlayer(object):
    # this person relies on player input
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
        print(self.cardDict)
        card = input("What value card do you want to play? ('pass' or 'out')")
        if card == 'out' or card == 'pass':
            return [card]
        else:
            card = int(card)
        if card == 2:
            self.cardDict[2] -= 1
            return [2, 1]
        if self.cardDict[3] > 0:
            three = input("Did you use a three? (y/n)")
            if three == 'y':
                amountOfThree = int(input("How many threes did you use?"))
                self.cardDict[3] -= amountOfThree
                self.cardDict[card] -= (cardsOnTop[1] - amountOfThree)
                return [card, cardsOnTop[1]]
        # if it hasn't returned by now they are just playing normally
        self.cardDict[card] -= cardsOnTop[1]
        return [card, cardsOnTop[1]]

    def start(self):
        print(self.cardDict)
        card = input("You are starting, what value card do you want to play? (or 'out)")
        if card == 'out':
            return [card]
        else:
            card = int(card)
        if card == 2:
            self.cardDict[2] -= 1
            return [2, 1]
        amount = int(input("How many of that card do you want to play? (including threes)"))
        if self.cardDict[3] > 0:
            three = input("Did you use a three? (y/n)")
            if three == 'y':
                amountOfThree = int(input("How many threes did you use?"))
                self.cardDict[3] -= amountOfThree
                self.cardDict[card] -= (amount - amountOfThree)
                return [card, amount]
        # if it hasn't returned by now they are just playing normally
        self.cardDict[card] -= amount
        return [card, amount]

    def giveLowestCard(self):
        print(self.cardDict)
        card = int(input("You are giving any one card away. What card?"))
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
