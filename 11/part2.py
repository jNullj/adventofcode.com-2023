from __future__ import annotations
import itertools
import os
import math

f = open(os.path.dirname(__file__) + "/input.txt", "r")

class Location:
    _static_id = 0

    def __init__(self,x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y
        self.id = Location._static_id
        Location._static_id += 1
    
    def distance(self, other: Location) -> int:
        distX = abs(self.x - other.x)
        distY = abs(self.y - other.y)
        return distX + distY

galaxyLocations: list[Location] = []
galaxyXDict: dict[int, list[Location]] = {}
XSIZE: int = None
YSIZE: int = None
EXPANSIONRATE = 1000000
y = 0
for line in f:
    if line == "\n":
        break
    if XSIZE == None:
        XSIZE = len(line)
    x = 0
    for char in line:
        if char == "#":
            newGalaxy = Location(x, y)
            galaxyLocations.append(newGalaxy)
            if x not in galaxyXDict.keys():
                galaxyXDict[x] = []    
            galaxyXDict[x].append(newGalaxy)
        x += 1
    if galaxyLocations[-1].y != y:
        y += EXPANSIONRATE-1 # due to cosmic expantion
    y += 1
YSIZE = y

#expend for x axis
offset = 0
for x in range(XSIZE):
    if x not in galaxyXDict.keys():
        offset += EXPANSIONRATE-1
        continue
    for galaxy in galaxyXDict[x]:
        galaxy.x += offset

sum = 0
for galaxy1, galaxy2 in itertools.combinations(galaxyLocations, 2):
    sum += galaxy1.distance(galaxy2)
    #print('Distance of', galaxy1.id+1, 'from', galaxy2.id+1, 'is', galaxy1.distance(galaxy2))
print(sum)