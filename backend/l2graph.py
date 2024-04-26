from backend.topic import Topic
from backend.edge import Edge

class L2Graph:
    def __init__(self, topics: list[Topic], edges: list[Edge]):
        self.topics: list[Topic] = topics
        self.edges: list[Edge] = edges
