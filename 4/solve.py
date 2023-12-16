from __future__ import annotations
import os

f = open(os.path.dirname(__file__) + "/input.txt", "r")

class Card:
    def __init__(self, winning: list[int] = [], recived: list[int] = []):
        self.winning_numbers = winning
        self.recived_numbers = recived

    def __init__(self, string: str):
        self.winning_numbers = []
        self.recived_numbers = []
        self.fromString(string, self)
    
    def addWining(self, num: int):
        self.winning_numbers.append(num)
    
    def addRecived(self, num: int):
        self.recived_numbers.append(num)

    @staticmethod
    def fromString(string: str, card: Card = None) -> Card:
        string = string.split(':')[1] # remove prefix
        array = string.split('|')
        winning_str = array[0]
        recived_str = array[1]
        winning = winning_str.split()
        recived = recived_str.split()
        if card is None:
            card = Card()
        for num in winning:
            card.addWining(int(num))
        for num in recived:
            card.addRecived(int(num))
        return card
    
    def points(self) -> int:
        count_winning = -1
        for num in self.recived_numbers:
            if num in self.winning_numbers:
                count_winning += 1
        if count_winning < 0:
            return 0
        return 2**count_winning


cards: list[Card] = []
for line in f:
    line = line[:-1] # remove \n
    cards.append(Card(line))

sum = 0
for card in cards:
    sum += card.points()
print(sum)