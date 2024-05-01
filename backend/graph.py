from backend.topic import Topic
from backend.paper import Paper
from backend.edge import Edge

class Graph:
    def __init__(self, l1_topics: list[Topic], l2_topics: list[Topic], edges: list[Edge], papers: list[Paper]):
        self.l1_topics: list[Topic] = l1_topics
        self.l2_topics: list[Topic] = l2_topics
        self.edges: list[Edge] = edges
        self.papers: list[Paper] = papers
