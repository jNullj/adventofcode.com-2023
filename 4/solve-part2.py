from __future__ import annotations
from functools import cached_property
import os
import re

f = open(os.path.dirname(__file__) + "/input.txt", "r")

class Card:
    def __init__(self, id: int = -1, winning: list[int] = [], recived: list[int] = []):
        self.id = id
        self.winning_numbers = winning
        self.recived_numbers = recived
        self.copies = 1

    def __init__(self, string: str):
        self.id = -1
        self.winning_numbers = []
        self.recived_numbers = []
        self.copies = 1
        self.fromString(string, self)
    
    def addWining(self, num: int):
        self.winning_numbers.append(num)
        self.__dict__.pop('numberOfWins', None)
    
    def addRecived(self, num: int):
        self.recived_numbers.append(num)
        self.__dict__.pop('numberOfWins', None)

    @staticmethod
    def fromString(string: str, card: Card = None) -> Card:
        if card is None:
            card = Card()

        string_arr = string.split(':')
        prefix = string_arr[0]
        numbers_str = string_arr[1]

        id = re.sub("[^0-9]", "", prefix)
        card.id = int(id) - 1

        array = numbers_str.split('|')
        winning_str = array[0]
        recived_str = array[1]
        winning = winning_str.split()
        recived = recived_str.split()
        for num in winning:
            card.addWining(int(num))
        for num in recived:
            card.addRecived(int(num))
        return card
    
    @cached_property
    def numberOfWins(self) -> int:
        wins = 0
        for num in self.recived_numbers:
            if num in self.winning_numbers:
                wins += 1
        return wins


cards: list[Card] = []
for line in f:
    line = line[:-1] # remove \n
    cards.append(Card(line))

for card in cards:
    if card.numberOfWins < 1:
        continue
    for i in range(card.id+1, min(card.id + card.numberOfWins+1,len(cards))):
        cards[i].copies += card.copies

sum = 0
for card in cards:
    sum += card.copies
print(sum)