from __future__ import annotations
from functools import cached_property
import os
import math

f = open(os.path.dirname(__file__) + "/input.txt", "r")

class Race:
    def __init__(self, raceTime: int, bestScore: int):
        self._time = raceTime   # milisec
        self._score = bestScore # milimeter

    @property
    def time(self):
        return self._time
    @property
    def bestScore(self):
        return self._score
    @property
    def acceleration(self):
        return 1    # 1 milimeter/milisec^2

    def currentScorePressTime(self) -> list[int]:
        # latex proof
        # bestscore = x, time = t, speed = v, accelerate  = a, press = p \\
        # x = v(t-p), v = ap \\
        # x = ap(t-p) \Rightarrow x = apt - ap^2 \Rightarrow ap^2 - atp + x = 0 \\
        # p_1 = \frac{at+\sqrt{a^2t^2-4ax}}{2a}, p_2 = \frac{a-+\sqrt{a^2t^2-4ax}}{2a}
        solutions: list[int] = []
        a = self.acceleration
        t = self.time
        x = self.bestScore

        p1 = (a*t - math.sqrt( (a*t)**2 - 4*a*x )) / (2*a)
        p2 = (a*t + math.sqrt( (a*t)**2 - 4*a*x )) / (2*a)

        solutions.append(p1)
        if p1 != p2:
            solutions.append(p2)

        return solutions
    
    def optimalPressTime(self) -> list[int]:
        # x = v(t-p), v  = ap => x=ap(t-p)=apt-ap^2
        # x' = at - 2ap => min at x' = 0 = at - 2ap
        # 2ap = at => p = t / 2
        t = self.time
        p = t / 2
        # due to discreate nature we might have 2 solutions
        result: list[int] = []
        if p.is_integer():
            result.append(p)
        else:
            result.append(math.floor(p))
            result.append(math.ceil(p))
        return result



raceTime: list[int] = []
bestScore: list[int] = []
for line in f:
    if line.startswith('Time'):
        num_str = "".join(line.split()[1:])
        raceTime = int(num_str)
    if line.startswith('Distance'):
        num_str = "".join(line.split()[1:])
        bestScore = int(num_str)

race: Race = Race(raceTime, bestScore)

winning_paths = (race.optimalPressTime()[0] -  math.floor(race.currentScorePressTime()[0]))*2
if len(race.optimalPressTime()) == 1:
    winning_paths -= 1
print(int(winning_paths))