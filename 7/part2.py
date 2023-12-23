from __future__ import annotations
from functools import cached_property
from enum import Enum
import os
import math

f = open(os.path.dirname(__file__) + "/input.txt", "r")

class Card():
    def __init__(self, cardCahr: str):
        self.__cardChar = cardCahr
    @staticmethod
    def __cardCahrToValue(char: str) -> int:
        if char.isdigit():
            return int(char)
        else:
            match char:
                case 'T':
                    return 10
                case 'J':
                    return 1
                case 'Q':
                    return 12
                case 'K':
                    return 13
                case 'A':
                    return 14
                case _:
                    raise ValueError
    @property
    def char(self) -> str:
        return self.__cardChar
    @cached_property
    def value(self) -> int:
        return self.__cardCahrToValue(self.char)
    def __eq__(self, other: Card|int|str) -> bool:
        if type(other).__name__ == 'Card':
            return self.value == other.value
        if type(other).__name__ == 'int':
            return self.value == other
        if type(other).__name__ == 'str':
            return self.char == other
        return TypeError
    def __ne__(self, other: Card|int|str) -> bool:
        return not self == other
    def __lt__(self, other: Card|int|str) -> bool:
        if type(other).__name__ == 'Card':
            return self.value < other.value
        return TypeError
    def __gt__(self, other: Card|int|str) -> bool:
        if type(other).__name__ == 'Card':
            return self.value < other.value
        return TypeError
    @property
    def isJoker(self):
        return self.char == 'J'
    
class Hand:
    class HANDS(Enum):
        FIVE_OF_A_KIND  = 7
        FOUR_OF_A_KIND  = 6
        FULL_HOUSE      = 5
        THREE_OF_A_KIND = 4
        TWO_PAIR        = 3
        ONE_PAIR        = 2
        HIGH_CARD       = 1
        def __lt__(self, other: Hand.HANDS) -> bool:
            if self.__class__ is other.__class__:
                return self.value < other.value
            raise TypeError
        def __gt__(self, other: Hand.HANDS) -> bool:
            if self.__class__ is other.__class__:
                return self.value > other.value
            raise TypeError
            

    def __init__(self, cards: list[Card]|str, bid: int = 0):
        match type(cards).__name__:
            case 'list':
                if len(cards) < 1:
                    raise ValueError
                if type(cards[0]) != Card:
                    raise TypeError
                self.__cards = cards.copy()
            case 'str':
                self.__cards = []
                for char in cards:
                    self.__cards.append(Card(char))
            case _:
                raise TypeError
        self.__bid = bid
    @property
    def cards(self):
        return self.__cards.copy()
    @property
    def bid(self):
        return self.__bid
    
    def __contains__(self, other: Card) -> bool:
        for card in self.cards:
            if card == other:
                return True
        return False

    @cached_property
    def type(self) -> int:
        cardFreq = {}
        jokers = 0
        for card in self.cards:
            if card.isJoker:
                jokers += 1
                continue
            if card.value in cardFreq.keys():
                cardFreq[card.value] += 1
            else:
                cardFreq[card.value] = 1
        numOfUniqueCards = max(len(cardFreq), 1)
        highestComboOfCards = max(cardFreq.values(), default=0) + jokers
        if numOfUniqueCards == 1:
            return self.HANDS.FIVE_OF_A_KIND
        if numOfUniqueCards == 2 and highestComboOfCards == 4:
            return self.HANDS.FOUR_OF_A_KIND
        if numOfUniqueCards == 2 and highestComboOfCards == 3:
            return self.HANDS.FULL_HOUSE
        if numOfUniqueCards == 3 and highestComboOfCards == 3:
            return self.HANDS.THREE_OF_A_KIND
        if numOfUniqueCards == 3 and highestComboOfCards == 2:
            return self.HANDS.TWO_PAIR
        if numOfUniqueCards == 4:
            return self.HANDS.ONE_PAIR
        if numOfUniqueCards == 5:
            return self.HANDS.HIGH_CARD
        raise RuntimeError
    
    def __lt__(self, other: Hand) -> bool:
        if self.type != other.type:
            return self.type < other.type
        if len(self.cards) != len(other.cards):
            raise ValueError
        for myCard, otherCard in zip(self.cards, other.cards):
            if myCard != otherCard:
                return myCard < otherCard
        return False
    def __gt__(self, other: Hand) -> bool:
        if self.type != other.type:
            return self.type > other.type
        if len(self.cards) != len(other.cards):
            raise ValueError
        for myCard, otherCard in zip(self.cards, other.cards):
            if myCard != otherCard:
                return myCard > otherCard
        return False
    def __eq__(self, other: Hand) -> bool:
        if len(self.cards) != len(other.cards):
            raise ValueError
        for myCard, otherCard in zip(self.cards, other.cards):
            if myCard != otherCard:
                return False
        return True
    def __ne__(self, other: Hand) -> int:
        return not self == other

hands: list[Hand] = []
for line in f:
    if line == '\n':
        break
    splittedLine = line.split()
    cards = splittedLine[0]
    bid = int(splittedLine[1])
    hands.append(Hand(cards, bid))
hands.sort()
sum = 0
for i, hand in enumerate(hands):
    sum += (i+1) * hand.bid
print(sum)