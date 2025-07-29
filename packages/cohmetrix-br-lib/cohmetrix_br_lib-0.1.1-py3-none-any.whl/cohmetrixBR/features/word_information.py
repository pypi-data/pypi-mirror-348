"""Word Information features.
"""
from __future__ import annotations

import numpy as np

from cohmetrixBR.utils import ModelPool

pool = ModelPool()


def WRDAOAc(text: str) -> float:
    """
    Age of acquisition for content words, mean

    MRC traduzido de https://websites.psychology.uwa.edu.au/school/MRCDatabase/mrc2.html
    """
    processed_text = pool.pre_processing_keep_stopword_lemma(text)
    average_aoa = 0
    number_content_words = 0
    for w in processed_text.split():
        try:
            aoa = pool.MRC['aoa'][pool.MRC_words.index(w)]
            if aoa > 0:
                average_aoa = average_aoa + aoa
                number_content_words = number_content_words + 1
        except:
            ...
    try:
        return average_aoa / number_content_words

    except:
        return 0.0


def WRDFAMc(text: str) -> float:
    """
    Familiarity for content words, mean

    MRC traduzido de https://websites.psychology.uwa.edu.au/school/MRCDatabase/mrc2.html
    """
    processed_text = pool.pre_processing_keep_stopword_lemma(text)
    average_fam = 0
    number_content_words = 0
    for w in processed_text.split():
        try:
            fam = pool.MRC['fam'][pool.MRC_words.index(w)]
            if fam > 0:
                average_fam = average_fam + fam
                number_content_words = number_content_words + 1
        except:
            ''
    try:
        return average_fam / number_content_words
    except:
        return 0.0


def WRDCNCc(text: str) -> float:
    """
    Concreteness for content words, mean

    MRC traduzido de https://websites.psychology.uwa.edu.au/school/MRCDatabase/mrc2.html
    """
    processed_text = pool.pre_processing_keep_stopword_lemma(text)
    average_conc = 0
    number_content_words = 0
    for w in processed_text.split():
        try:
            conc = pool.MRC['conc'][pool.MRC_words.index(w)]
            if conc > 0:
                average_conc = average_conc + conc
                number_content_words = number_content_words + 1
        except:
            ''
    try:
        return average_conc / number_content_words
    except:
        return 0.0


def WRDIMGc(text: str) -> float:
    """
    Imageability for content words, mean

    MRC traduzido de https://websites.psychology.uwa.edu.au/school/MRCDatabase/mrc2.html
    """
    processed_text = pool.pre_processing_keep_stopword_lemma(text)
    average_imag = 0
    number_content_words = 0
    for w in processed_text.split():
        try:
            imag = pool.MRC['imag'][pool.MRC_words.index(w)]
            if imag > 0:
                average_imag = average_imag + imag
                number_content_words = number_content_words + 1
        except:
            ''
    try:
        return average_imag / number_content_words
    except:
        return 0.0


def WRDMEAc(text: str) -> float:
    """
    Meaningfulness, Colorado norms, content words, mean.

    MRC traduzido de https://websites.psychology.uwa.edu.au/school/MRCDatabase/mrc2.html
    """
    processed_text = pool.pre_processing_keep_stopword_lemma(text)
    average_meanc = 0
    number_content_words = 0
    for w in processed_text.split():
        try:
            meanc = pool.MRC['meanc'][pool.MRC_words.index(w)]
            if meanc > 0:
                average_meanc = average_meanc + meanc
                number_content_words = number_content_words + 1
        except:
            pass
    try:
        return average_meanc / number_content_words
    except:
        return 0.0


def WRDFRQc(text: str) -> float:
    """
    ...
    """
    processed_text = pool.pre_processing_keep_stopword_token(text)
    frequency_content_word = 0
    number_content_words = 0
    for w in processed_text.split():
        try:
            frequency_content_word = frequency_content_word + \
                pool.cbow_s50.wv.vocab[w].count
            number_content_words = number_content_words + 1
        except:
            pass
    try:
        return (frequency_content_word / number_content_words) / 139592
    except:
        return 1.0


def WRDFRQa(text: str):
    """
    ...
    """
    return np.log(WRDFRQc(text))


def WRDFRQmc(text: str) -> float:
    """
    ...
    """
    processed_text = pool.pre_processing_keep_stopword_token(text)
    frequency_content_word = 0
    number_content_words = len(processed_text.split())
    for w in processed_text.split():
        try:
            frequency_content_word = frequency_content_word + \
                pool.cbow_s50.wv.vocab[w].count
        except:
            ''
    try:
        return (frequency_content_word / number_content_words) / 139592
    except:
        return 0.0


def WRDPRP1s(text: str) -> int:
    """
    First person singular pronoun incidence.
    """
    return pool.word_count(text, 'eu')


def WRDPRP1p(text: str) -> int:
    """
    First person plural pronoun incidence.
    """
    return pool.word_count(text, 'nós')


def WRDPRP2s(text: str) -> int:
    """
    Second person singular pronoun incidence.
    """
    return pool.word_count(text, 'tu') + pool.word_count(text, 'você')


def WRDPRP2p(text: str) -> int:
    """
    Second person plural pronoun incidence.
    """
    return pool.word_count(text, 'vós') + pool.word_count(text, 'vocês')


def WRDPRP3s(text: str) -> int:
    """
    Third person singular pronoun incidence.
    """
    return pool.word_count(text, 'ele') + pool.word_count(text, 'ela')


def WRDPRP3p(text: str) -> int:
    """
    Third person plural pronoun incidence.
    """
    return pool.word_count(text, 'eles') + pool.word_count(text, 'elas')


def WRDNOUN(text: str) -> int:
    """
    Noun incidence.
    """
    doc = pool.nlp(text)

    noun_count = 0
    for token in doc:
        if token.pos_ == "NOUN":
            noun_count += 1

    return noun_count


def WRDVERB(text: str) -> int:
    """
    Verb incidence.
    """
    doc = pool.nlp(text)

    verb_count = 0
    for token in doc:

        if token.pos_ == "VERB":
            verb_count += 1

    return verb_count


def WRDADJ(text: str) -> int:
    """
    Adjective incidence.
    """
    doc = pool.nlp(text)

    adjective_count = 0
    for token in doc:
        if token.pos_ == "ADJ":
            adjective_count += 1

    return adjective_count


def WRDADV(text: str) -> int:
    """
    Adverb incidence.
    """
    doc = pool.nlp(text)

    adverb_count = 0
    for token in doc:
        if token.pos_ == "ADV":
            adverb_count += 1

    return adverb_count


def WRDPRO(text: str) -> int:
    """
    Pronoun incidence.
    """
    doc = pool.nlp(text)

    pronoun_count = 0
    for token in doc:
        if token.pos_ == "PRON":
            pronoun_count += 1

    return pronoun_count


def WRDPRP2(text: str) -> int:
    return WRDPRP2s(text) + WRDPRP2p(text)

FEATURES = [
    WRDNOUN,
    WRDVERB,
    WRDADJ,
    WRDADV,
    WRDPRO,
    WRDPRP1s,
    WRDPRP1p,
    WRDPRP2,
    WRDPRP2s,
    WRDPRP2p,
    WRDPRP3s,
    WRDPRP3p,
    WRDFRQc,
    WRDFRQa,
    WRDFRQmc,
    WRDAOAc,
    WRDFAMc,
    WRDCNCc,
    WRDIMGc,
    WRDMEAc,
]
