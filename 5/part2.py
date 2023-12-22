from __future__ import annotations
from functools import cached_property
import os
import math

f = open(os.path.dirname(__file__) + "/input.txt", "r")

class Seed:
    def __init__(self, num: int) -> None:
        self.num = num

class PropRange:
    def __init__(self, num: int, size: int) -> None:
        self.num = num
        self.size = size
    def __iter__(self):
        self.iterVal = self.num
        return self
    def __next__(self):
        if self.iterVal <= self.last:
            val = self.iterVal
            self.iterVal += 1
            return Seed(val)
        else:
            raise StopIteration
    def __lt__(self, other):
            return self.last < other.num
    def __add__(self, other):
        if type(other).__name__ == 'int':
            return PropRange(self.num + other, self.size)
        raise TypeError
    def __rshift__(self, other):
        if self.num >= other:
            raise ValueError
        delta = other - self.num
        return [PropRange(self.num, delta), PropRange(other, self.size - delta)]
    def __lshift__(self, other):
        if self.last <= other:
            raise ValueError
        delta = self.last - other
        return [PropRange(other+1, self.size - delta - 1), PropRange(self.num, delta)]
    def __contains__(self, val):
        if val >= self.num and val <= self.last:
            return True
        return False
    @cached_property
    def last(self):
        return self.num + self.size - 1
    
class SeedRange(PropRange):
    def __init__(self, num: int, size: int) -> None:
        super().__init__(num, size)
    def toPropRange(self):
        return PropRange(self.num, self.size)

class Map:
    def __init__(self, source: str, destination: str) -> None:
        self.source = source
        self.destination = destination
        self.rules: self.Rule = []
        self.linkedSourceMap = None
    
    def translate(self, source: int | Seed | SeedRange) -> int:
        if type(source).__name__ == 'SeedRange':
            return self.translateRange(source)
        int_source = 0
        if self.linkedSourceMap is not None and type(source).__name__ == 'Seed':
            int_source = self.linkedSourceMap.translate(source)
        elif type(source).__name__ == 'Seed' and self.source == 'seed':
            int_source = source.num
        for rule in self.rules:
            if int_source >= rule.from_source and int_source <= rule.to_source:
                return rule.translate(int_source)

        return int_source
    
    def translateRange(self, source: SeedRange) -> list[PropRange]:
        if self.linkedSourceMap is not None and type(source).__name__ == 'SeedRange':
            range_source = self.linkedSourceMap.translateRange(source)
        elif type(source).__name__ == 'SeedRange' and self.source == 'seed':
            range_source = [source.toPropRange()]
        resultsTranslated: list[PropRange] = []
        resultsUntranslated: list[PropRange] = range_source.copy()
        for rule in self.rules:
            copySource = resultsUntranslated.copy()
            resultsUntranslated = []
            for pRange in copySource:
                if pRange.num > rule.to_source or pRange.last < rule.from_source:
                    resultsUntranslated.append(pRange)
                    continue
                elif pRange.num >= rule.from_source and pRange.last <= rule.to_source:
                    resultsTranslated.append(rule.translate(pRange))
                    continue
                # range collision
                splited: PropRange = []
                if pRange.num < rule.from_source and pRange.last >= rule.from_source:
                    splited = pRange >> rule.from_source
                if pRange.num <= rule.to_source and pRange.last > rule.to_source:
                    if len(splited) > 0:
                        splited = [splited[0]] + (splited[1] << rule.to_source)
                    else:
                        splited = pRange << rule.to_source
                match len(splited):
                    case 0:
                        raise ValueError
                    case 1:
                        raise ValueError
                    case 2:
                        if pRange.num < rule.from_source and pRange.last >= rule.from_source:
                            resultsUntranslated.append(splited[0])
                            resultsTranslated.append(rule.translate(splited[1]))
                        elif pRange.num <= rule.to_source and pRange.last > rule.to_source:
                            resultsUntranslated.append(splited[0])
                            resultsTranslated.append(rule.translate(splited[1]))
                        else:
                            raise ValueError
                    case 3:
                        resultsUntranslated.append(splited[0])
                        resultsUntranslated.append(splited[1])
                        resultsTranslated.append(rule.translate(splited[2]))
        return resultsUntranslated + resultsTranslated
    
    def addRule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def addRule(self, from_source: int, from_dest: int, range: int) -> None:
        rule = self.Rule(from_sour, from_dest, range)
        self.rules.append(rule)

    def setSourceMap(self, map: Map) -> None:
        self.linkedSourceMap = map
    
    class Rule:
        def __init__(self, start_source: int, start_destination: int, range: int) -> None:
            self.from_source = start_source
            self.from_destination = start_destination
            self.range = range

        def __lt__(self, other):
            return self.to_destination < other.to_destination
        
        @cached_property
        def to_source(self) -> int:
            return self.from_source + self.range - 1
        
        @cached_property
        def to_destination(self) -> int:
            return self.from_destination + self.range - 1
        
        @cached_property
        def translationShift(self) -> int:
            return self.from_destination - self.from_source

        def translate(self, source: int | PropRange) -> int:
            return source + self.translationShift

segments: list[str] = []
text_buffer = ""
for line in f:
    if line == "\n":
        segments.append(text_buffer)
        text_buffer = ""
        continue
    text_buffer += line
if text_buffer != "":
    segments.append(text_buffer)
    del text_buffer

seeds_strings = segments[0][:-1].split()[1:]
seeds: list[SeedRange] = []
for i in range(0, len(seeds_strings), 2):
    seeds.append(SeedRange(int(seeds_strings[i]), int(seeds_strings[i+1])))

maps_strings = segments[1:]
maps: list[Map] = []
for map_string in maps_strings:
    source_dest_str = map_string.splitlines()[0].split()[0].split('-')
    source = source_dest_str[0]
    dest = source_dest_str[2]
    newMap = Map(source, dest)
    for line in map_string.splitlines()[1:]:
        ruleVals = line.split()
        from_dest = int(ruleVals[0])
        from_sour = int(ruleVals[1])
        range = int(ruleVals[2])
        newMap.addRule(from_sour, from_dest, range)
    maps.append(newMap)
for map in maps:
    for otherMap in maps:
        if map.source == otherMap.destination:
            map.setSourceMap(otherMap)
            break

lastMap = list(filter(lambda m: m.destination == 'location', maps))[0]
locations_range: PropRange = []
idx = 1
for seed_range in seeds:
    locations_range += lastMap.translate(seed_range)
    idx += 1
min_locations: list[int] = []
for location in locations_range:
    # minimum location of locations range is first num
    min_locations.append(location.num)
print(min(min_locations))