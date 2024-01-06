from __future__ import annotations
from functools import cached_property
import itertools
import os
from enum import StrEnum

f = open(os.path.dirname(__file__) + "/input.txt", "r")

def clamp(lower: int, val: int, upper: int) -> int:
    return min(upper, max(val, lower))

class Location:
    LOCATION_SIZE_LIMIT = 100000 # used for non-colliedable hashing of Location, Must be multi of 10

    def __init__(self, x: int, y: int) -> None:
        if x >= Location.LOCATION_SIZE_LIMIT \
        or y >= Location.LOCATION_SIZE_LIMIT:
            raise ValueError("x,y coordingates must be smaller then LOCATION_SIZE_LIMIT="+str(Location.LOCATION_SIZE_LIMIT))
        self.x = x
        self.y = y
    def above(self, l: Location) -> bool:
        return self.y < l.y and self.x == l.x
    def below(self, l: Location) -> bool:
        return self.y > l.y and self.x == l.x
    def rightOf(self, l: Location) -> bool:
        return self.x > l.x and self.y == l.y
    def leftOf(self, l: Location) -> bool:
        return self.x < l.x and self.y == l.y
    def __eq__(self, other: Location) -> bool:
        if not isinstance(other, Location):
            return False
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True
    def __hash__(self) -> int:
        return self.x + Location.LOCATION_SIZE_LIMIT * self.y

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
    CORNERS = {TYPES.UP_LEFT, TYPES.UP_RIGHT, TYPES.DOWN_LEFT, TYPES.DOWN_RIGHT}
    
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
        for pipeline in pipes:
            for pipe in pipeline:
                if type(pipe) is not Pipe:
                    continue
                if pipe.type == Pipe.TYPES.START:
                    self.start = pipe
        self.setAdjacent()
        self.loopLocations = self.findLoop()
        startType = self.findStartPipeType()
        self.pipeReplace(self.start.location, Pipe(startType))

    @property
    def sizeX(self) -> int:
        return len(self.pipes[0])
    @property
    def sizeY(self) -> int:
        return len(self.pipes)

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
    
    def isInLoop(self, l: Location) -> bool:
        if not hasattr(self, '_isInLoopCache'):
            self._isInLoopCache = {}
        if l in self._isInLoopCache:
            return self._isInLoopCache[l]
        result = l in self.loopLocations
        self._isInLoopCache[l] = result
        return result
    
    def pipeReplace(self, l: Location, newPipe: Pipe) -> None:
        self.pipes[l.y][l.x] = newPipe
        newPipe.location = l
        if self.start.location == l:
            self.start = newPipe
    
    def setAdjacent(self) -> None:
        for pipeLine in self.pipes:
            for pipe in pipeLine:
                if pipe == None:
                    continue
                for location in pipe.adjacentLocations():
                    if not self.inRange(location):
                        continue
                    if self.isEmpty(location):
                        continue
                    if self.pipeAt(location).type in pipe.allowedConnection(location):
                        pipe.addAdjacent(self.pipeAt(location))

    def findLoop(self) -> list[Location]:
        loopOrderedLocations: list[Location] = []
        start = self.start
        for adj in start.adjacent:
            prevPipe = start
            currentPipe = adj
            loopOrderedLocations = []
            loopOrderedLocations.append(start.location)
            while currentPipe is not start and currentPipe != None:
                temp = currentPipe
                loopOrderedLocations.append(currentPipe.location)
                currentPipe = currentPipe.nextInPath(prevPipe)
                prevPipe = temp
            if currentPipe == None:
                continue
            if currentPipe is start:
                break
            raise RuntimeError
        return loopOrderedLocations
    
    def findStartPipeType(self) -> Pipe.TYPES:
        this = self.start.location
        next = self.loopLocations[1]
        prev = self.loopLocations[-1]
        if this.y != next.y and this.y != prev.y:
            return Pipe.TYPES.VERTICAL
        if this.x != next.x and this.x != prev.x:
            return Pipe.TYPES.HORIZONTAL
        if next.above(this) and prev.rightOf(this):
            return Pipe.TYPES.UP_RIGHT
        if prev.above(this) and next.rightOf(this):
            return Pipe.TYPES.UP_RIGHT
        if next.above(this) and prev.leftOf(this):
            return Pipe.TYPES.UP_LEFT
        if prev.above(this) and next.leftOf(this):
            return Pipe.TYPES.UP_LEFT
        if next.below(this) and prev.rightOf(this):
            return Pipe.TYPES.DOWN_RIGHT
        if prev.below(this) and next.rightOf(this):
            return Pipe.TYPES.DOWN_RIGHT
        if next.below(this) and prev.leftOf(this):
            return Pipe.TYPES.DOWN_LEFT
        if prev.below(this) and next.leftOf(this):
            return Pipe.TYPES.DOWN_LEFT
        raise RuntimeError
    
    def isEnclosed(self, l: Location) -> bool:
        xEnclosed = False
        yEnclosed = False
        if self.isInLoop(l):
            # if on loop cant be enclosed
            return False
        lastCorner = None
        for x in range(l.x):
            testLocation = Location(x, l.y)
            if not self.isInLoop(testLocation):
                continue
            testedPipe = self.pipeAt(testLocation)
            if testedPipe.type == Pipe.TYPES.VERTICAL:
                xEnclosed = not xEnclosed
                continue
            if testedPipe.type in Pipe.CORNERS:
                if lastCorner == None:
                    xEnclosed = not xEnclosed
                    lastCorner = testedPipe
                    continue
                elif (lastCorner.type in Pipe.TOP_CONNECTED  and testedPipe.type in Pipe.TOP_CONNECTED) \
                or (lastCorner.type in Pipe.BOT_CONNECTED  and testedPipe.type in Pipe.BOT_CONNECTED):
                    xEnclosed = not xEnclosed
                lastCorner = None
        lastCorner = None
        for y in range(l.y):
            testLocation = Location(l.x, y)
            if not self.isInLoop(testLocation):
                continue
            testedPipe = self.pipeAt(testLocation)
            if testedPipe.type == Pipe.TYPES.HORIZONTAL:
                yEnclosed = not yEnclosed
                continue
            if testedPipe.type in Pipe.CORNERS:
                if lastCorner == None:
                    yEnclosed = not yEnclosed
                    lastCorner = testedPipe
                    continue
                elif (lastCorner.type in Pipe.LEFT_CONNECTED  and testedPipe.type in Pipe.LEFT_CONNECTED) \
                or (lastCorner.type in Pipe.RIGHT_CONNECTED  and testedPipe.type in Pipe.RIGHT_CONNECTED):
                    yEnclosed = not yEnclosed
                lastCorner = None
        if xEnclosed and yEnclosed:
            return True
        return False



pipes: list[list[Pipe| None]] = list()
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

enclosed = 0
for x,y in itertools.product(range(mynet.sizeX), range(mynet.sizeY)):
    testLocation = Location(x, y)
    if mynet.isEnclosed(testLocation):
        enclosed += 1

def rainbowS(i: int):
    cycle = int(i/255)%3
    val  = i%255
    r = 0
    g = 0
    b = 0
    match cycle:
        case 0:
            r = val
            b = 255 - val
        case 1:
            g = val
            r = 255 - val
        case 2:
            b = val
            g = 255 - val
    return ""+str(r)+";"+str(g)+";"+str(b)

#printme
printer = ""
x = 0
y = 0
step = 0
for pline in mynet.pipes:
    for p in pline:
        pLocation = Location(x, y)
        if mynet.isEnclosed(pLocation):
            printer += '\x1b[48;2;0;255;0m'
            if p == None:
                printer += '.'
            else:
                printer += p.type.value
            printer += '\x1b[0m'
        elif mynet.isInLoop(pLocation):
            printer += '\x1b[38;2;'+rainbowS(mynet.loopLocations.index(pLocation)*5)+'m'
            match p.type:
                case Pipe.TYPES.DOWN_LEFT:
                    printer += "┓"
                case Pipe.TYPES.HORIZONTAL:
                    printer += "━"
                case Pipe.TYPES.VERTICAL:
                    printer += "┃"
                case Pipe.TYPES.DOWN_RIGHT:
                    printer += "┏"
                case Pipe.TYPES.UP_LEFT:
                    printer += "┛"
                case Pipe.TYPES.UP_RIGHT:
                    printer += "┗"
            printer += '\x1b[0m'
            step += 5
        else:
            printer += '\x1b[48;2;255;0;0m'
            if p == None:
                printer += '.'
            else:
                printer += p.type.value
            printer += '\x1b[0m'
        x += 1
    printer += "\n"
    y += 1
    x = 0
print(printer)


print(enclosed)