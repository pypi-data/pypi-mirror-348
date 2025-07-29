"""Syntactic Pattern Density features.
"""
from cohmetrixBR.utils import ModelPool

pool = ModelPool()


def DRNP(text: str) -> int:
    """
    Incidência de frases nominais.
    @:parameter: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)
    words = 0
    fn = 0

    for sent in doc.sents:
        for token in sent:
            words += 1
            if token.dep_ == "ROOT":
                if token.pos_ == "NOUN":
                    fn += 1
    ifn = fn
    return ifn


def DRVP(text: str) -> int:
    """
    Incidência de frases verbais.
    @:parameter: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)
    words = 0
    fn = 0

    for sent in doc.sents:
        for token in sent:
            words += 1
            if token.dep_ == "ROOT":
                if token.pos_ == "VERB":
                    fn += 1
    ifn = fn
    return ifn


def DRAP(text: str) -> int:
    """
    Incidência de frases adverbiais.
    @:parameter: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)
    words = 0
    fn = 0

    for sent in doc.sents:
        for token in sent:
            words += 1
            if token.dep_ == "ROOT":
                if token.pos_ == "ADV":
                    fn += 1
    ifn = fn
    return ifn


def DRPP(text: str) -> int:
    """
    Incidência de frases preposicionais.
    @:parameter: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)
    words = 0
    fn = 0

    for sent in doc.sents:
        for token in sent:
            words += 1
            if token.dep_ == "ROOT":
                if token.pos_ == "ADP":
                    fn += 1
    ifn = fn
    return ifn


def DRPVAL(text: str) -> int:
    """
    Incidência de agentes da passiva.
    @:parameter: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)
    words = 0
    fn = 0

    for sent in doc.sents:
        for token in sent:
            words += 1
            if "pass" in str(token.dep_):
                fn += 1
    ifn = fn
    return ifn


def DRNEG(text: str) -> int:
    """
    Incidência de expressões de negação.
    @:parameter: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)
    words = 0
    fn = 0

    for sent in doc.sents:
        for token in sent:
            words += 1

            if token.dep_ == "neg":
                fn += 1
    ifn = fn
    return ifn


def DRGERUND(text: str) -> int:
    """
    Incidência de gerúndio.
    @:parameter: texto -> text
    @:returns:   npd  -> number, mean
    """
    gerund_pt = ["ando", "endo", "indo"]
    doc = pool.nlp(text)
    words = 0
    fn = 0

    for sent in doc.sents:
        for token in sent:
            words += 1
            if token.pos_ == "VERB":
                if token.text[-4:] in gerund_pt:
                    fn += 1

    ifn = fn
    return ifn


def DRINF(text: str) -> int:
    """
    Incidência de Infinitivo.
    @:parameter: texto -> text
    @:returns:   npd  -> number, mean
    """
    infinitive_pt = ["ar", "er", "ir"]
    doc = pool.nlp(text)
    words = 0
    fn = 0

    for sent in doc.sents:
        for token in sent:
            words += 1
            if token.pos_ == "VERB":
                if token.text[-2:] in infinitive_pt:
                    fn += 1
    ifn = fn
    return ifn


FEATURES = [
    DRNP,
    DRVP,
    DRAP,
    DRPP,
    DRPVAL,
    DRNEG,
    DRGERUND,
    DRINF,
]
