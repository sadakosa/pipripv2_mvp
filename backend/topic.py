class Topic:
    def __init__(self, d):
        self.type = "Topic"
        self.id = d.get("id")
        self.description = ""  # TODO: generate topic summary
