import json

class Topic:
    def __init__(self, topic_ID, topic_type, topic_title, topic_exp, topic_ref):
        self.ID = topic_ID #integer ID
        self.type = topic_type #level 2 are fundamental topics, level 1 are categories
        self.title = topic_title #the title
        self.exp = topic_exp #the word explanation
        self.ref = topic_ref #list of references
