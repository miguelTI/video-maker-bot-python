import json
from Sentence import Sentence
import pickle


class Content:
    def __init__(self):
        self.search_term = None
        self.prefix = None
        self.source_content = None
        self.source_content_sanitized = None
        self.sentences = []
        self.downloaded_images = []

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def load_json(self, file_path):
        with open(file_path, 'r') as content_data:
            self.__dict__ = json.load(content_data)
            if len(self.sentences) > 0:
                for key, sentence in enumerate(self.sentences, start=0):
                    new_sentence = Sentence()
                    new_sentence.text = sentence["text"]
                    new_sentence.images = sentence["images"]
                    new_sentence.keywords = sentence["keywords"]
                    self.sentences[key] = new_sentence

    @staticmethod
    def load(file_path):
        with open(file_path, 'rb') as fp:
            return pickle.load(fp)

    def save(self, file_path):
        with open(file_path, 'wb') as fp:
            pickle.dump(self, fp, protocol=pickle.HIGHEST_PROTOCOL)
