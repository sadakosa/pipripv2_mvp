class Topic:
    def __init__(self, d):
        self.id = d.get("id")
        self.description = d.get("description", "No description found.")
