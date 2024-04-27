class Edge:
    def __init__(self, d):
        self.source_type = d.get("source_type")
        self.target_type = d.get("target_type")
        self.source = d.get("source")
        self.target = d.get("target")
        self.label = d.get("label")
