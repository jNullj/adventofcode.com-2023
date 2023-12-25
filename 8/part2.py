from __future__ import annotations
from functools import cached_property
import os

f = open(os.path.dirname(__file__) + "/input.txt", "r")

class Node:
    def __init__(self, name: str, left: Node=None, right: Node=None):
        self.__name = name
        self.__left = left
        self.__right = right
    @property
    def name(self) -> str:
        return self.__name
    @property
    def right(self) -> Node:
        return self.__right
    @right.setter
    def right(self, node: Node) -> None:
        if node.__class__ is not self.__class__:
            raise TypeError
        self.__right = node
    @property
    def left(self) -> Node:
        return self.__left
    @left.setter
    def left(self, node: Node) -> None:
        if node.__class__ is not self.__class__:
            raise TypeError
        self.__left = node
    def __eq__(self, other: Node) -> bool:
        if self.__class__ != other.__class__:
            raise TypeError
        return self.name == other.name
    @cached_property
    def isStart(self):
        return self.name.endswith('A')
    @cached_property
    def isEnd(self):
        return self.name.endswith('Z')

instructions: str = ""
nodes: dict[str, Node] = {}
nodes_connections_str: dict[str, str] = {}
for i, line in enumerate(f):
    if line == "\n" and i > 1:
        break
    if i == 0:
        instructions = line[:-1]
    if i > 1:
        nodeName = line.split()[0]
        newNode = Node(nodeName)
        nodes[nodeName] = newNode
        conStr = "".join(line[:-1].split()[2:4])
        nodes_connections_str[nodeName] = conStr
for name, conStr in nodes_connections_str.items():
    splitted = conStr.split(',')
    left = splitted[0][1:]
    right = splitted[1][:-1]
    nodes[name].left = nodes[left]
    nodes[name].right = nodes[right]

currentNodes: list[Node] = []
for node in nodes.values():
    if node.isStart:
        currentNodes.append(node)


firstEncounter: list[int] = []
firstName: list[str] = []
loopCounter: list[int] = []
loopName: list[str] = []
for node in currentNodes:
    currentNode = node
    steps = 0
    endFlag = 0
    while endFlag < 2:
        for char in instructions:
            match char:
                case 'L':
                    currentNode = currentNode.left
                case 'R':
                    currentNode = currentNode.right
                case _:
                    raise ValueError
            steps += 1
            if currentNode.isEnd:
                if endFlag == 0:
                    firstEncounter.append(steps)
                    firstName.append(currentNode.name)
                else:
                    loopCounter.append(steps)
                    loopName.append(currentNode.name)
                steps = 0
                endFlag += 1
                if endFlag > 1:
                    break
def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)
next = max(loopCounter)
for i in loopCounter:
    result = gcd(next, i)
    mult = i * next
    next = mult/result
print(int(next))
