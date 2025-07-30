from enum import Enum
from typing import List

class Color(Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2

class GraphNode:
    def __init__(self, val):
        self.val = val
        self.edges = []
        self.color = Color.WHITE

    def add_edges(self, nodes: List['GraphNode']):
        for node in nodes:
            self.edges.append(node)

    def __str__(self):
        return str(self.val)
