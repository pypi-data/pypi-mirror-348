"""Lexical diversity features.
"""
from lexical_diversity import lex_div as ld

from cohmetrixBR.utils import ModelPool

pool = ModelPool()


def LDTTRc(text: str):
    """
    Lexical diversity, type-token ratio, content word lemmas
    @:params: texto -> text
    @:returns:   ttr  -> number, type-token ratio
    """
    doc = pool.nlp(text)

    word_list = []
    for sent in doc.sents:
        for token in sent:
            if token.pos_ in {"NOUN", "VERB", "ADV", "ADJ"}:
                word_list.append(str(token.lemma_))

    unique_words = set(word_list)

    try:
        return len(unique_words) / len(word_list)
    except:
        return 0


def LDTTRa(text: str):
    """
    Lexical diversity, type-token ratio, all words
    @:params: texto -> text
    @:returns:   ttr  -> number, type-token ratio
    """
    doc = pool.nlp(text)

    word_list = []
    for sent in doc.sents:
        for token in sent:
            if token.pos_ != "PUNCT":
                word_list.append(str(token))

    unique_words = set(word_list)

    try:
        return len(unique_words) / len(word_list)
    except:
        return 0


def LDMTLDa(text: str):
    doc = pool.nlp(text)

    word_list = []
    for sent in doc.sents:
        for token in sent:
            if token.pos_ != "PUNCT":
                word_list.append(str(token))

    return ld.mtld(word_list)


def LDVOCDa(text: str):
    doc = pool.nlp(text)

    word_list = []
    for sent in doc.sents:
        for token in sent:
            if token.pos_ != "PUNCT":
                word_list.append(str(token))

    return ld.hdd(word_list)


FEATURES = [
    LDTTRc,
    LDTTRa,
    LDMTLDa,
    LDVOCDa
]
