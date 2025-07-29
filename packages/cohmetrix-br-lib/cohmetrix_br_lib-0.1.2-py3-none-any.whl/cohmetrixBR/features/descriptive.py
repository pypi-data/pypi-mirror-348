"""Descriptive features.
"""
import numpy as np

from cohmetrixBR.utils import ModelPool

pool = ModelPool()


def DESPC(text: str) -> int:
    """
    Paragraph count, number of paragraphs.
    Função conta a quantidade de parágrafos em um texto.
    Parâmetros: text -> Array de textos.
    Retorno: n -> Inteiro, quantidade de parágrafos.
    @SrtaCamelo
    """
    n = text.count('\n\n') + 1
    return n


def DESPC2(text: str) -> int:
    """
    Paragraph count, number of paragraphs.
    Função conta a quantidade de parágrafos em um texto.
    Parâmetros: text -> Array de textos.
    Retorno: n -> Inteiro, quantidade de parágrafos.
    @SrtaCamelo
    """
    n = text.count('\n') + 1
    return n


def DESSC(text: str) -> int:
    """
    Sentence count, number of sentences.
    Função conta a quantidade de frases em um texto.
    Parâmetros: text -> Array de textos.
    Retorno: n -> Inteiro, quantidade de frases.
    @SrtaCamelo
    """
    sent_text = pool.sent_tokenize(text)
    n = len(sent_text)
    return n


def DESWC(text: str) -> int:
    """
    Word count, number of words.
    Função conta a quantidade de palavras em um texto.
    Parâmetros: text -> Array de textos.
    Retorno: n -> Inteiro, quantidade de palavras.
    @SrtaCamelo
    """
    tokenized_text = pool.word_tokenize(text)
    n = len(tokenized_text)
    return n


def DESPL(text: str) -> float:
    """
    Paragraph length, number of sentences, mean.
    """
    sentences_per_paragraph = pool.phrases_per_paragraph(text)
    return np.mean(sentences_per_paragraph)


def DESPLd(text: str) -> float:
    """
    Paragraph length, number of sentences, standard deviation.
    """
    sentences_per_paragraph = pool.phrases_per_paragraph(text)
    return np.std(sentences_per_paragraph)


def DESSL(text: str) -> float:
    """
    Sentence length, number of words, mean.
    """
    words_per_sentence = pool.words_per_sentence(text)
    return np.mean(words_per_sentence)


def DESSLd(text: str) -> float:
    """
    Sentence length, number of words, standard deviation.
    """
    words_per_sentence = pool.words_per_sentence(text)
    return np.std(words_per_sentence)


def DESWLsy(text: str) -> float:
    """
    Word length, number of syllables, mean.
    """
    count_syllables = []
    words = pool.word_tokenize(text)

    for word in words:
        count_syllables.append(pool.syllables_per_word(word))

    return np.mean(count_syllables)


def DESWLsyd(text: str) -> float:
    """
    Word length, number of syllables, standard deviation
    """
    count_syllables = []
    words = pool.word_tokenize(text)

    for word in words:
        count_syllables.append(pool.syllables_per_word(word))

    return np.std(count_syllables)


def DESWLlt(text: str) -> float:
    """Word length, number of letters, mean"""
    letters_per_word = pool.chars_per_word(text)
    return np.mean(letters_per_word)


def DESWLltd(text: str) -> float:
    """Word length, number of letters, standard deviation"""
    letters_per_word = pool.chars_per_word(text)
    return np.std(letters_per_word)


FEATURES = [
    DESPC,
    DESPC2,
    DESPL,
    DESPLd,
    DESSC,
    DESSL,
    DESSLd,
    DESWC,
    DESWLsy,
    DESWLsyd,
    DESWLlt,
    DESWLltd,
]
