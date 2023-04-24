import os
from contextlib import redirect_stdout

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from athena.nlu.base import IntentClassificationBase


class NLTKIntentClassification(IntentClassificationBase):
    def __init__(self, **kwargs):
        self.use_svm = kwargs.pop("use_svm", False)
        super().__init__(**kwargs)

        with redirect_stdout(open(os.devnull, "w")):
            nltk.download("punkt")
            nltk.download("stopwords")
        self.stemmer = SnowballStemmer("english")
        self.stop_words = set(stopwords.words("english"))
        self._model: Pipeline = None  # type: ignore

    def train(self, training_data):
        if self.use_svm:
            pipeline = self.train_with_svm(training_data)
        else:
            pipeline = self.train_with_multinomial_nb(training_data)
        self._model = pipeline
        return pipeline

    def train_with_svm(self, training_data):
        sentences, intents = training_data
        X_train, X_test, y_train, y_test = train_test_split(
            sentences, intents, test_size=0.1, random_state=42
        )

        # Create a pipeline with TfidfVectorizer and an SVM classifier
        pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer()),
                ("clf", SVC(kernel="linear", probability=True)),
            ]
        )
        # Train the classifier
        for _ in range(10):
            pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        print(classification_report(y_test, y_pred))
        return pipeline

    def train_with_multinomial_nb(self, training_data):
        vectorizer = TfidfVectorizer(
            tokenizer=self.tokenize_and_preprocess, ngram_range=(1, 2)
        )
        classifier = MultinomialNB(alpha=0.85)
        pipeline = Pipeline([("vectorizer", vectorizer), ("classifier", classifier)])

        texts, intents = zip(*training_data)
        pipeline.fit(texts, intents)
        return pipeline

    def process(self, text):
        return self.predict_intent_with_confidence(text)

    def predict_intent(self, text):
        return self._model.predict([text])[0]

    def predict_intent_with_confidence(self, text):
        intent_probabilities = self._model.predict_proba([text])[0]
        intent_index = intent_probabilities.argmax()
        confidence_score = intent_probabilities[intent_index]
        predicted_intent = self._model.classes_[intent_index]

        return predicted_intent, confidence_score

    def predict_intents_with_confidence(self, text):
        intent_probabilities = self._model.predict_proba([text])[0]
        intents_confidence = sorted(
            zip(self._model.classes_, intent_probabilities),
            key=lambda x: x[1],
            reverse=True,
        )

        return intents_confidence

    def __call__(self, text):
        return self.process(text)

    def tokenize_and_preprocess(self, text):
        tokens = nltk.word_tokenize(text)
        filtered_tokens = [token for token in tokens if token not in self.stop_words]
        stemmed_tokens = [self.stemmer.stem(token) for token in filtered_tokens]
        return stemmed_tokens
