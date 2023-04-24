import os
from contextlib import redirect_stdout

import nltk
from nltk import ne_chunk, pos_tag
from nltk.tokenize import word_tokenize

from athena.nlu.base import EntityExtractionBase


class NLTKEntityExtraction(EntityExtractionBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._model = None
        with redirect_stdout(open(os.devnull, "w")):
            nltk.download("punkt")
            nltk.download("maxent_ne_chunker")
            nltk.download("words")
            nltk.download("averaged_perceptron_tagger")

    def train(self, training_data):
        pass

    def process(self, text):
        return self.predict_entities(text)

    def predict_entities(self, text):
        words = word_tokenize(text)
        pos_tags = pos_tag(words)
        named_entities_tree = ne_chunk(pos_tags, binary=False)
        named_entities = []

        for tree_node in named_entities_tree:
            if isinstance(tree_node, nltk.tree.Tree):
                entity_type = tree_node.label()
                entity_name = " ".join([token for token, pos in tree_node.leaves()])
                named_entities.append((entity_type, entity_name))

        return named_entities
