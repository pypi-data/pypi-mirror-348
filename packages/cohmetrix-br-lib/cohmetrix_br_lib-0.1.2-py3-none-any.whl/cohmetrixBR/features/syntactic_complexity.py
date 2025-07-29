"""Syntactic complexity features.
"""
from collections import Counter

import numpy as np

from cohmetrixBR.utils import ModelPool

pool = ModelPool()


def edit_distance(s1, s2):
    diferences = 0

    n = min(len(s1), len(s2))
    for i in range(n):
        if str(s1[i]) != str(s2[i]):
            diferences += 1

    med = diferences / n
    return med


def SYNLE(text: str) -> float:
    """
    Left embeddedness, words before main verb, mean.
    @:parameter: text -> text
    @:returns:   lemb  -> number, mean
    """
    doc = pool.nlp(text)

    lemb = 0
    s_idx = -1
    for sent in doc.sents:
        s_idx += 1
        for idx, token in enumerate(sent):
            if token.dep_ == "ROOT":
                lemb += idx
    lemb = lemb / (s_idx + 1)
    return lemb


def SYNNP(text: str) -> float:
    doc = pool.nlp(text)
    modifiers = 0
    noun_phrases = []

    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "ROOT":
                # print(token, token.pos_)
                if token.pos_ == "NOUN":
                    noun_phrases.append(sent)

    for sent in noun_phrases:
        for token in sent:
            if token.pos_ == "ADJ" or token.pos_ == "ADV":
                modifiers += 1

    if not noun_phrases:
        return 0

    return modifiers / len(noun_phrases)


def SYNMEDpos(text: str) -> float:
    """
    Minimal Edit Distance, part of speech, mean.
    @:parameter: texto -> text
    @:returns:   medm  -> number, mean
    """

    doc = pool.nlp(text)

    sentences = []
    for sent in doc.sents:
        sentence = []
        for token in sent:
            sentence.append(token.pos_)
        sentences.append(sentence)

    n_sents = len(sentences)
    if n_sents == 1:
        return 0

    med = []
    for i in range(n_sents - 1):
        medm = edit_distance(sentences[i], sentences[i + 1])
        med.append(medm)

    return np.mean(med)


def SYNMEDlem(text: str) -> float:
    """
    Minimal Edit Distance, lemmas, mean.
    @:parameter: texto -> text
    @:returns:   medm  -> number, mean
    """
    doc = pool.nlp(text)

    sentences = []
    for sent in doc.sents:
        sentence = []
        for token in sent:
            sentence.append(token.lemma)
        sentences.append(sentence)

    n_sents = len(sentences)
    if n_sents == 1:
        return 0

    med = []
    for i in range(n_sents - 1):
        medm = edit_distance(sentences[i], sentences[i + 1])
        med.append(medm)

    return np.mean(med)


def SYNMEDwrd(text: str) -> float:
    """
    Minimal Edit Distance, all words
    @:parameter: texto -> text
    @:returns:   medm  -> number, mean
    """
    doc = pool.nlp(text)

    sentences = []
    for sent in doc.sents:
        sentence = []
        for token in sent:
            sentence.append(token)
        sentences.append(sentence)

    n_sents = len(sentences)
    if n_sents == 1:
        return 0

    med = []
    for i in range(n_sents - 1):
        medm = edit_distance(sentences[i], sentences[i + 1])
        med.append(medm)

    return np.mean(med)


def SYNSTRUTa(text: str) -> float:
    sentences = pool.sent_tokenize(text)

    syntactic_similarity = []
    for i in range(0, len(sentences) - 1):
        doc1 = pool.nlp(sentences[i])
        doc2 = pool.nlp(sentences[i + 1])
        dep1 = Counter([word.dep_ for word in doc1])
        dep2 = Counter([word.dep_ for word in doc2])
        syntactic_similarity.append(pool.cosine_similarity(dep1, dep2))

    if syntactic_similarity:
        return np.mean(syntactic_similarity)
    return 0.0


def SYNSTRUTt(text: str) -> float:
    paragraphs = text.split("\n")
    syntactic_similarity = [
        SYNSTRUTa(paragraph) for paragraph in paragraphs
    ]
    return np.mean(syntactic_similarity)


FEATURES = [
    SYNLE,
    SYNNP,
    SYNMEDpos,
    SYNMEDlem,
    SYNMEDwrd,
    SYNSTRUTa,
    SYNSTRUTt,
]
