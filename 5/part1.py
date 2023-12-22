from __future__ import annotations
from functools import cached_property
import os

f = open(os.path.dirname(__file__) + "/input.txt", "r")

class Seed:
    def __init__(self, num: int) -> None:
        self.num = num
    def __init__(self, num: str) -> None:
        self.num = int(num)

class Map:
    def __init__(self, source: str, destination: str) -> None:
        self.source = source
        self.destination = destination
        self.rules: self.Rule = []
        self.linkedSourceMap = None
    
    def translate(self, source: int | Seed) -> int:
        int_source = 0
        if self.linkedSourceMap is not None and type(source).__name__ == 'Seed':
            int_source = self.linkedSourceMap.translate(source)
        elif type(source).__name__ == 'Seed' and self.source == 'seed':
            int_source = source.num
        for rule in self.rules:
            if int_source >= rule.from_source and int_source <= rule.to_source:
                return rule.translate(int_source)

        return int_source
    
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

        def translate(self, source: int) -> int:
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
seeds = list(map(Seed, seeds_strings))

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
locations: list[int] = []
for seed in seeds:
    locations.append(lastMap.translate(seed))

print(min(locations))