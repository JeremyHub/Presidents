import math
import random

class Player(object):
    def __init__(self, name):
        self.name = name
        self.startingHand = []
        self.valHand = []

    def sortHand(self):
        for card in self.startingHand:
            self.valHand.append(card.value)
        self.valHand.sort()

    # Draw n number of cards from a given deck
    def draw(self, deck, num=1):
        for i in range(num):
            self.startingHand.append(deck.draw())

    def showValHand(self):
        return self.valHand

    def showHand(self):
        return self.startingHand

    def play(self, cardsOnTop):
        typeOfTrick = len(cardsOnTop)

        if cardsOnTop == [] or cardsOnTop == 'out':
            cardsOnTop = [0]

        # checks if already out
        if len(self.valHand) == 0:
            return ["out"]

        if typeOfTrick == 1:
            # loops through hand
            for i in range(0, len(self.valHand), 1):
                possibleCard = self.valHand[i]
                # checks if card in loop is a valid card to play, continues if not
                if possibleCard >= cardsOnTop[0] and self.valHand[i] != 2 and self.valHand[i] != 3:
                    self.valHand.remove(possibleCard)
                    return [possibleCard]

            # second loop, loops through valHand backwards to play any threes then twos
            for i in range(len(self.valHand)-1, -1, -1):
                possibleCard = self.valHand[i]
                # checks if the card on top is not an ace, otherwise plays a three
                # this might be strategically bad idk
                if possibleCard == 3 and cardsOnTop[0] != 14:
                    self.valHand.remove(possibleCard)
                    # if it has gotten to here then the hand has a 3 to play, and it plays it as an ace
                    return [14]
                # this plays a two, if it gets to here then it cant play anything else
                if possibleCard == 2:
                    self.valHand.remove(possibleCard)
                    # should always return a 2
                    return [possibleCard]
            return ["pass"]

    def start(self):
        # this 15 should be changed to lower card later, bc if not then the player is out
        possibleCard = 15
        # checks to see if out
        if len(self.valHand) == 0:
            return ["out"]

        # loops backwards through hand
        for i in range(len(self.valHand)-1, -1, -1):
            # checks if the card its looking at is less than possibleCard and not 2's or 3's
            if self.valHand[i] < possibleCard and self.valHand[i] != 2 and self.valHand[i] != 3:
                possibleCard = self.valHand[i]
                possibleCard = self.valHand[i]
            # if the above for loop didnt change from 15 then only 2's and or 3's are left
            if possibleCard == 15:
                for i in range(0, len(self.valHand), 1):
                    if self.valHand[i] < possibleCard and self.valHand != 2:
                        possibleCard = self.valHand[i]
            # if the above loop also didnt change from 15 then only 2's remain in the hand
            if possibleCard == 15:
                possibleCard = 2
        self.valHand.remove(possibleCard)
        return [possibleCard]