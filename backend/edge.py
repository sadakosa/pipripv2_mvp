class Edge:
    def __init__(self, d):
        self.source = d.get("source")
        self.target = d.get("target")
        self.label = d.get("label")
