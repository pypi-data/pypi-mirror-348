"""Situation features.
"""
from cohmetrixBR.features import connectives as connectives
from cohmetrixBR.utils import ModelPool

pool = ModelPool()


def SMINTEp(text: str):
    doc = pool.nlp(text)
    intentional_verb = 0
    for token in doc:
        if token.lemma_ in pool.intentional_verbs:
            intentional_verb = intentional_verb + 1
    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return intentional_verb / quociente
    else:
        return intentional_verb / (1 + quociente)


def SMINTEp_sentence(text: str):
    sentences = pool.sent_tokenize(text)
    intentional_verb_sentences = 0

    for s in sentences:
        if SMINTEp(s) > 0:
            intentional_verb_sentences = intentional_verb_sentences + 1

    return intentional_verb_sentences


def SMINTEr(text: str):
    intentional_verb = SMINTEp(text)
    intentional_sentences = SMINTEp_sentence(text)
    return intentional_sentences / (intentional_verb + 1)


def SMCAUSwn(text: str):
    doc = pool.nlp(text)
    verbs = [word.lemma_
             for word in doc
             if word.pos_ == "VERB"]

    if len(verbs) == 0:
        return 0

    synonyms = []
    for verb in verbs:
        for word_set in pool.wordnet:
            if word_set.__contains__(verb):
                synonyms.extend(word_set)

    synonyms = [x.lower() for x in synonyms]
    intersection = len(list(set(synonyms) & set(verbs)))
    size = len(text.split())
    quotient = size // 1000
    remainder = size % 1000

    if remainder == 0:
        return intersection / quotient
    else:
        return intersection / (1 + quotient)


FEATURES = [
    SMINTEp,
    SMINTEp_sentence,
    SMINTEr,
    SMCAUSwn,
]
