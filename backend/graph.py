from backend.topic import Topic
from backend.paper import Paper
from backend.edge import Edge

class Graph:
    def __init__(self, topics: list[Topic], edges: list[Edge], papers: list[Paper]):
        self.topics: list[Topic] = topics
        self.edges: list[Edge] = edges
        self.papers: list[Paper] = papers
