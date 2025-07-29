"""Referential Cohesion features.
"""
import numpy as np
from nltk.stem import RSLPStemmer

from cohmetrixBR.utils import ModelPool

pool = ModelPool()


def CRFNO1(text: str) -> int:
    """
    Noun overlap, adjacent sentences, binary, mean
    @:params: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)
    # nouns_in_previous_sentence
    nps = []

    # Count of sentences that have the same noun as previous sentence
    sentence_count = 0

    for sent in doc.sents:
        # nouns_in_actual_sentence
        nas = []
        for token in sent:
            if token.pos_ == "NOUN":
                nas.append(str(token))

        if any(i in nps for i in nas):
            sentence_count += 1
        nps = nas

    return sentence_count


def CRFAO1(text: str) -> int:
    """
    Argument overlap, adjacent sentences, binary, mean
    @:params: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)

    # nouns_in_previous_sentence
    nps = []

    # Count of sentences that have the same noun as previous sentence
    sentence_count = 0

    for sent in doc.sents:
        # nouns_in_actual_sentence
        nas = []

        for token in sent:
            if token.pos_ == "NOUN":
                nas.append(str(token.lemma_))
            elif token.pos_ == "PRON":
                nas.append(str(token))

        if any(i in nps for i in nas):
            sentence_count += 1
        nps = nas

    return sentence_count


def CRFSO1(text: str) -> int:
    """
    Stem overlap, adjacent sentences, binary, mean
    @:params: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)
    # contentWords_in_previous_sentence
    cps = []
    stemmer = RSLPStemmer()

    # Count of sentences that have the
    #   same noun as previous sentence
    sentence_count = 0

    for sent in doc.sents:
        # nouns_in_actual_sentence
        nas = []

        # contentWords_in_actual_sentence
        cas = []

        for token in sent:
            if token.pos_ == "NOUN":
                stem = stemmer.stem(str(token))
                nas.append(stem)

            stem = stemmer.stem(str(token))
            cas.append(stem)

        if any(i in cps for i in nas):
            sentence_count += 1

        cps = cas

    return sentence_count


def CRFNOa(text: str) -> int:
    """
    Noun overlap, all sentences, binary, mean
    @:params: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)

    # nouns_in_previous_sentence
    nps = []

    # nouns_in_actual_sentence
    nas = []

    # Count of sentences that have the
    #   same noun as previous sentence
    sentence_count = 0

    all_sentences = [sent for sent in doc.sents]

    for i in range(len(all_sentences)):
        for j in range(len(all_sentences)):
            if j > i:

                for token in all_sentences[i]:
                    if token.pos_ == "NOUN":
                        nps.append(str(token))
                for token in all_sentences[j]:
                    if token.pos_ == "NOUN":
                        nas.append(str(token))

                if any(i in nps for i in nas):
                    sentence_count += 1
                nps, nas = [], []

    return sentence_count


def CRFAOa(text: str) -> int:
    """
    Noun overlap, all sentences, binary, mean
    @:params: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)

    # nouns_in_previous_sentence
    nps = []

    # nouns_in_actual_sentence
    nas = []

    # Count of sentences that have
    #   the same noun as previous sentence
    sentence_count = 0

    all_sentences = [sent for sent in doc.sents]

    for i in range(len(all_sentences)):
        for j in range(len(all_sentences)):
            if j > i:
                for token in all_sentences[i]:
                    if token.pos_ == "NOUN":
                        nps.append(str(token.lemma_))
                    elif token.pos_ == "PRON":
                        nps.append(str(token))

                for token in all_sentences[j]:
                    if token.pos_ == "NOUN":
                        nas.append(str(token.lemma_))
                    elif token.pos_ == "PRON":
                        nas.append(str(token))

                if any(i in nps for i in nas):
                    sentence_count += 1

                nps, nas = [], []

    return sentence_count


def CRFSOa(text: str) -> int:
    """
    Stem overlap, all sentences, binary, mean
    @:params: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)

    # contentWord_in_previous_sentence
    cps = []

    # nouns_in_actual_sentence
    nas = []
    stemmer = RSLPStemmer()

    # Count of sentences that have
    #   the same noun as previous sentence
    sentence_count = 0

    all_sentences = [sent for sent in doc.sents]

    for i in range(len(all_sentences)):
        for j in range(len(all_sentences)):
            if j > i:
                for token in all_sentences[i]:
                    stem = stemmer.stem(str(token))
                    cps.append(stem)

                for token in all_sentences[j]:
                    if token.pos_ == "NOUN":
                        stem = stemmer.stem(str(token))
                        nas.append(stem)

                if any(i in cps for i in nas):
                    sentence_count += 1
                cps, nas = [], []

    return sentence_count  # /len(all_sentences)


def CRFCWO1(text: str) -> float:
    """
    Content word overlap, adjacent sentences, proportional, mean
    @:params: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)

    # contentWords_in_previous_sentence
    cps = []

    # List of Proportions
    proportions = []

    for sent in doc.sents:
        # contentWords_in_actual_sentence
        cas = []

        for token in sent:
            if token.pos_ != "PUNCT":
                cas.append(str(token))

        if len(cps) != 0:
            overlaps = len(set(cps) & set(cas))
            nWords = len(cps) + len(cas)
            proportions.append((overlaps / nWords))

        cps = cas

    if len(proportions) > 0:
        return np.mean(proportions)

    return 0.0


def CRFCWO1d(text: str) -> float:
    """
    Content word overlap, adjacent sentences, proportional, standard deviation
    @:params: texto -> text
    @:returns:   npd  -> number, STD
    """
    doc = pool.nlp(text)

    # contentWords_in_previous_sentence
    cps = []

    # List of Proportions
    proportions = []

    for sent in doc.sents:
        # contentWords_in_actual_sentence
        cas = []

        for token in sent:
            if token.pos_ != "PUNCT":
                cas.append(str(token))

        if len(cps) != 0:
            overlaps = len(set(cps) & set(cas))
            nWords = len(cps) + len(cas)
            proportions.append((overlaps / nWords))

        cps = cas

    if len(proportions) > 0:
        return np.std(proportions)

    return 0.0


def CRFCWOa(text: str) -> float:
    """
    Content word overlap, all sentences, proportional, mean
    @:params: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)

    # contentWords_in_previous_sentence
    cps = []

    # contentWords_in_actual_sentence
    cas = []

    # List of Proportions
    proportions = []

    all_sentences = [sent for sent in doc.sents]

    if len(all_sentences) == 1:
        return 0

    for i in range(len(all_sentences)):
        for j in range(len(all_sentences)):
            if j > i:
                for token in all_sentences[i]:
                    if token.pos_ != "PUNCT":
                        cps.append(str(token))

                for token in all_sentences[j]:
                    if token.pos_ != "PUNCT":
                        cas.append(str(token))

                overlaps = len(set(cps) & set(cas))
                nWords = len(cps) + len(cas)
                try:
                    proportions.append((overlaps / nWords))
                except:
                    proportions.append(0)

                cps, cas = [], []

    return np.mean(proportions)


def CRFCWOad(text: str) -> float:
    """
    Content word overlap, all sentences, proportional, standard deviation
    @:params: texto -> text
    @:returns:   npd  -> number, mean
    """
    doc = pool.nlp(text)

    # contentWords_in_previous_sentence
    cps = []

    # contentWords_in_actual_sentence
    cas = []

    # List of Proportions
    proportions = []

    all_sentences = [sent for sent in doc.sents]

    if len(all_sentences) == 1:
        return 0

    for i in range(len(all_sentences)):
        for j in range(len(all_sentences)):
            if j > i:
                for token in all_sentences[i]:
                    if token.pos_ != "PUNCT":
                        cps.append(str(token))

                for token in all_sentences[j]:
                    if token.pos_ != "PUNCT":
                        cas.append(str(token))

                overlaps = len(set(cps) & set(cas))
                nWords = len(cps) + len(cas)

                try:
                    proportions.append((overlaps / nWords))
                except:
                    proportions.append(0)

                cps, cas = [], []

    return np.std(proportions)


FEATURES = [
    CRFNO1,
    CRFAO1,
    CRFSO1,
    CRFNOa,
    CRFAOa,
    CRFSOa,
    CRFCWO1,
    CRFCWO1d,
    CRFCWOa,
    CRFCWOad,
]
