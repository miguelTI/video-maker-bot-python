import json


class Content:
    def __init__(self):
        self.searchTerm = None
        self.prefix = None
        self.sourceContent = None
        self.sourceContentSanitized = None
        self.sentences = []

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def add_sentence(self, sentence):
        self.sentences.append(sentence)
