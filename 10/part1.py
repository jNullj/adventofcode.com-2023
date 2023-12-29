from __future__ import annotations
from functools import cached_property
import os
from enum import StrEnum

f = open(os.path.dirname(__file__) + "/input.txt", "r")

def clamp(lower: int, val: int, upper: int) -> int:
    return min(upper, max(val, lower))

class Location:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Pipe:
    class TYPES(StrEnum):
        VERTICAL = "|"
        HORIZONTAL = "-"
        UP_RIGHT = "L"
        UP_LEFT = "J"
        DOWN_LEFT = "7"
        DOWN_RIGHT = "F"
        START = "S"

    TOP_CONNECTED = {TYPES.VERTICAL, TYPES.UP_LEFT, TYPES.UP_RIGHT, TYPES.START}
    BOT_CONNECTED = {TYPES.VERTICAL, TYPES.DOWN_LEFT, TYPES.DOWN_RIGHT, TYPES.START}
    LEFT_CONNECTED = {TYPES.HORIZONTAL, TYPES.UP_LEFT, TYPES.DOWN_LEFT, TYPES.START}
    RIGHT_CONNECTED = {TYPES.HORIZONTAL, TYPES.UP_RIGHT, TYPES.DOWN_RIGHT, TYPES.START}
    
    def __init__(self, type: Pipe.TYPES, location: Location = None) -> None:
        self.type = type
        self.location = location
        self.adjacent: list[Pipe] = []
    
    def adjacentLocations(self) -> (Location, Location, Location|None, Location|None):
        x = self.location.x
        y = self.location.y
        match self.type:
            case Pipe.TYPES.VERTICAL:
                return (Location(x, y-1), Location(x, y+1))
            case Pipe.TYPES.HORIZONTAL:
                return (Location(x-1, y), Location(x+1, y))
            case Pipe.TYPES.UP_RIGHT:
                return (Location(x, y-1), Location(x+1, y))
            case Pipe.TYPES.UP_LEFT:
                return (Location(x, y-1), Location(x-1, y))
            case Pipe.TYPES.DOWN_LEFT:
                return (Location(x, y+1), Location(x-1, y))
            case Pipe.TYPES.DOWN_RIGHT:
                return (Location(x, y+1), Location(x+1, y))
            case Pipe.TYPES.START:
                return (Location(x,y+1), Location(x,y-1), Location(x+1,y), Location(x-1,y))
        return RuntimeError
    
    def allowedConnection(self, l: Location) -> dict[Pipe.TYPES]:
        match self.type:
            case Pipe.TYPES.VERTICAL:
                if l.y < self.location.y:
                    return Pipe.BOT_CONNECTED
                if l.y > self.location.y:
                    return Pipe.TOP_CONNECTED
            case Pipe.TYPES.HORIZONTAL:
                if l.x > self.location.x:
                    return Pipe.LEFT_CONNECTED
                if l.x < self.location.x:
                    return Pipe.RIGHT_CONNECTED
            case Pipe.TYPES.UP_RIGHT:
                if l.y < self.location.y:
                    return Pipe.BOT_CONNECTED
                if l.x > self.location.x:
                    return Pipe.LEFT_CONNECTED
            case Pipe.TYPES.UP_LEFT:
                if l.y < self.location.y:
                    return Pipe.BOT_CONNECTED
                if l.x < self.location.x:
                    return Pipe.RIGHT_CONNECTED
            case Pipe.TYPES.DOWN_LEFT:
                if l.y > self.location.y:
                    return Pipe.TOP_CONNECTED
                if l.x < self.location.x:
                    return Pipe.RIGHT_CONNECTED
            case Pipe.TYPES.DOWN_RIGHT:
                if l.y > self.location.y:
                    return Pipe.TOP_CONNECTED
                if l.x > self.location.x:
                    return Pipe.LEFT_CONNECTED
            case Pipe.TYPES.START:
                if l.y > self.location.y:
                    return Pipe.TOP_CONNECTED
                if l.x > self.location.x:
                    return Pipe.LEFT_CONNECTED
                if l.y < self.location.y:
                    return Pipe.BOT_CONNECTED
                if l.x < self.location.x:
                    return Pipe.RIGHT_CONNECTED
                
        return RuntimeError
    
    def addAdjacent(self, pipe: Pipe) -> None:
        self.adjacent.append(pipe)

    def followPath(self, prev: Pipe|None = None, steps: int = 0) -> int:
        if prev != None and prev.type == self.TYPES.START and steps > 1:
            return steps-1
        if prev == None and self.type == self.TYPES.START:
            for adj in self.adjacent:
                res = adj.followPath(self, steps+1)
                if res == None:
                    continue
                return res
        return self.nextInPath(prev).followPath(self, steps+1)
    
    def nextInPath(self, prev: Pipe) -> Pipe:
        if type(prev) is not Pipe:
            raise ValueError
        if self.type == self.TYPES.START:
            raise ValueError
        for adj in self.adjacent:
            if adj is not prev:
                return adj
        

class PipeNet:
    def __init__(self, pipes) -> None:
        self.pipes: list[list[Pipe| None]] = pipes

    def inRange(self, l: Location) -> bool:
        if l.x < 0:
            return False
        if l.y < 0:
            return False
        if l.y > len(self.pipes) - 1:
            return False
        if l.x > len(self.pipes[0]) - 1:
            return False
        return True
    
    def isEmpty(self, l: Location) -> bool:
        return self.pipes[l.y][l.x] == None
    
    def pipeAt(self, l: Location) -> Pipe:
        return self.pipes[l.y][l.x]
    
    def setAdjacent(self) -> None:
        for pipeLine in self.pipes:
            for pipe in pipeLine:
                if pipe is None:
                    continue
                for location in pipe.adjacentLocations():
                    if not self.inRange(location):
                        continue
                    if self.isEmpty(location):
                        continue
                    if self.pipeAt(location).type in pipe.allowedConnection(location):
                        pipe.addAdjacent(self.pipeAt(location))


pipes: list[list[Pipe| None]] = list()
start: Pipe = None
y = 0
for line in f:
    if line == "\n":
        break
    lineList: list[Pipe|None] = list()
    x = 0
    for char in line:
        match char:
            case "S":
                start = Pipe(Pipe.TYPES(char), Location(x, y))
                lineList.append(start)
            case ".":
                lineList.append(None)
            case "|" | "-" | "L" | "J" | "7" | "F":
                lineList.append(Pipe(Pipe.TYPES(char), Location(x, y)))
            case _:
                ValueError
        x += 1
    pipes.append(lineList)
    y += 1

mynet = PipeNet(pipes)
mynet.setAdjacent()

steps = 0
for adj in start.adjacent:
    prevPipe = start
    currentPipe = adj
    steps = 1
    while currentPipe is not start and currentPipe != None:
        temp = currentPipe
        currentPipe = currentPipe.nextInPath(prevPipe)
        prevPipe = temp
        steps += 1
    if currentPipe == None:
        continue
    if currentPipe is start:
        break
    raise RuntimeError

print(int(steps / 2))