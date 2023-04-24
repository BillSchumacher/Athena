class IntentClassificationBase:
    def train(self, training_data):
        raise NotImplementedError

    def process(self, text):
        raise NotImplementedError

    def predict_intent(self, text):
        raise NotImplementedError

    def predict_intent_with_confidence(self, text):
        raise NotImplementedError

    def predict_intents_with_confidence(self, text):
        raise NotImplementedError

    def __call__(self, text):
        return self.process(text)


class EntityExtractionBase:
    def train(self, training_data):
        raise NotImplementedError

    def process(self, text):
        raise NotImplementedError

    def predict_entities(self, text):
        raise NotImplementedError

    def __call__(self, text):
        return self.process(text)
