from __future__ import annotations
from functools import cached_property
import os

f = open(os.path.dirname(__file__) + "/input.txt", "r")

class ValueHistory:
    def __init__(self, string: str|None = None) -> None:
        self.vals = []
        if string != None:
            self.vals = list(map(int, string.split()))
    
    def addVal(self, val: int) -> None:
        self.vals.append(val)
    
    def differential(self) -> ValueHistory:
        result = ValueHistory()
        for a, b in zip(self.vals[:-1], self.vals[1:]):
            result.addVal(b - a)
        return result
    
    @property
    def isZeros(self) -> bool:
        for x in self.vals:
            if x != 0:
                return False
        return True
    @property
    def lastVal(self) -> int:
        return self.vals[-1]
    @property
    def firstVal(self) -> int:
        return self.vals[0]
    
    def nextVal(self) -> int:
        diffrentials: list[ValueHistory] = []
        diffrentials.append(self)
        while not diffrentials[-1].isZeros:
            diffrentials.append(diffrentials[-1].differential())
        diffrentials.reverse()
        result = 0
        for v in diffrentials[1:]:
            result = v.lastVal + result
        return result
    
    def preVal(self) -> int:
        diffrentials: list[ValueHistory] = []
        diffrentials.append(self)
        while not diffrentials[-1].isZeros:
            diffrentials.append(diffrentials[-1].differential())
        diffrentials.reverse()
        result = 0
        for v in diffrentials[1:]:
            result = v.firstVal - result
        return result
    
sum = 0
for line in f:
    if line == "\n":
        break
    sum += ValueHistory(line).preVal()
print(sum)