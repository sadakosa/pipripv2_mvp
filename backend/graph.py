from backend.topic import Topic
from backend.paper import Paper
from backend.edge import Edge

class Graph:
    def __init__(self, topics: list[Topic], edges: list[Edge]):
        self.topics: list[Topic] = topics
        self.edges: list[Edge] = edges

class L2Graph(Graph):
    def __init__(self, topics: list[Topic], papers: list[Paper], edges: list[Edge]):
        super().__init__(topics, edges)
        self.papers = papers

class L1Graph(Graph):
    def __init__(self, topics: list[Topic], edges: list[Edge]):
        super().__init__(topics, edges)
