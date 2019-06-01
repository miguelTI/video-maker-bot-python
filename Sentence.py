class Sentence:
    def __init__(self):
        self.text = None
        self.keywords = []
        self.images = []

    def add_keyword(self, keyword):
        self.keywords.append(keyword)

    def add_image(self, image):
        self.images.append(image)
