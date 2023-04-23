import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example
from loguru import logger


def train_intent_classifier(train_data):
    logger.debug("Training intent classifier...")
    nlp = spacy.load("en_core_web_md")
    textcat = nlp.create_pipe("textcat_multilabel") #, config={"architecture": "bow"})
    logger.debug("Adding textcat pipe...")
    #nlp.add_pipe(textcat, last=True)
    all_intents = []
    for _, annotations in train_data:
        for intent in annotations["intent"]:
            logger.debug(f"Adding label {intent} to textcat pipe...")
            textcat.add_label(intent)
            all_intents.append(intent)
    all_intents = list(set(all_intents))
    optimizer = nlp.create_optimizer()
    batch_size = compounding(4.0, 32.0, 1.001)
    logger.debug("Starting training...")
    default_intents = {intent: 0.0 for intent in all_intents}
    for i in range(10):
        losses = {}
        batches = minibatch(train_data, size=batch_size)
        logger.debug(f"Starting epoch {i}...")
        for batch in batches:
            texts, annotations = zip(*batch)
            logger.debug(f"Updating model with batch of {len(texts)} texts...")
            examples = []
            for a, annotation in enumerate(annotations):
                text = texts[a]
                doc = nlp.make_doc(text)
                logger.debug(f"Doc: {doc} Annotation: {annotation}")
                cats = default_intents.copy()
                for intent in annotation["intent"]:
                    cats[intent] = 1.0
                doc.cats = cats
                example = Example.from_dict(doc, {"cats": cats})
                logger.debug(f"Example: {example}")
                #logger.debug(f"Annotations: {annotations}  Texts: {text}  Optimizer: {optimizer}  Losses: {losses}")
                examples.append(example)
            nlp.update(examples, sgd=optimizer, drop=0.2, losses=losses)
    nlp.to_disk("trained_nlp")
    return nlp


def predict_intent(trained_nlp, text):
    doc = trained_nlp(text)
    intents = doc.cats
    logger.debug(f"Doc: {doc} Intents: {intents}  Sorted Intents: {sorted(intents.items(), key=lambda x: x[1], reverse=True)}")
    sorted_intents = sorted(intents.items(), key=lambda x: x[1], reverse=True)
    return sorted_intents[0][0] if sorted_intents else None
