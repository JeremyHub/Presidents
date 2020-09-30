import math
import random

values = {
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace"
}

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def show(self):
        return "{} of {}".format(values.get(self.value), self.suit)


class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        for card in self.cards:
            return card.show()

    # Generate 52 cards
    def build(self):
        for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
            for val in range(2, 15):
                self.cards.append(Card(suit, val))

    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Returns and pops the top card
    def draw(self):
        return self.cards.pop()
