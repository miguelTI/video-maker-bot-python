import json


class Content:
    def __init__(self):
        self.search_term = None
        self.prefix = None
        self.source_content = None
        self.source_content_sanitized = None
        self.sentences = []

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def add_sentence(self, sentence):
        self.sentences.append(sentence)
