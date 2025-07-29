"""Readability features.
"""
from cohmetrixBR.features.descriptive import DESWLsy
from cohmetrixBR.features.word_information import WRDFRQmc
from cohmetrixBR.features.referential_cohesion import CRFCWO1
from cohmetrixBR.features.syntactic_complexity import SYNSTRUTa
from cohmetrixBR.utils import ModelPool

pool = ModelPool()


def RDFRE(text: str) -> float:
    """
    Flesch Reading Ease.
    Returns a number from 0 to 100, with a higher score indicating easier reading.
    """
    sentence_count = len(pool.sent_tokenize(text))

    text = pool.pre_processing_keep_stopword_token(text)
    words = pool.word_tokenize(text)
    word_count = 0
    for words in words:
        word_count += 1

    # Average Sentence Length
    ASL = word_count / sentence_count

    # Average number of syllables per Word (CELEX in the original)
    ASW = DESWLsy(text)
    readfre = 206.835 - (1.015 * ASL) - (84.6 * ASW)

    return readfre


def RDFKGL(text: str) -> float:
    """
    Flesch-Kincaid Grade Level.
    The grade levels range from 0 to 12.
    The higher the number, the harder it is to read the text. 
    """

    sentence_count = len(pool.sent_tokenize(text))

    text = pool.pre_processing_keep_stopword_token(text)
    words = pool.word_tokenize(text)
    word_count = len(words)

    # Average Sentence Length
    ASL = word_count / sentence_count

    # Average number of Silabes per Word (CELEX in the original)
    ASW = DESWLsy(text)

    readfkgl = (.39 * ASL) + (11.8 * ASW) - 15.59

    return readfkgl


def RDL2(text: str) -> float:
    return -45.032 + \
        (52.230 * CRFCWO1(text) +
         (61.306 * SYNSTRUTa(text)) +
         22.205 * WRDFRQmc(text))


def smog_index(text: str):
    sentences = len(pool.sent_tokenize(text))

    if sentences >= 3:
        try:
            poly_syllables = pool.syllables_per_word(text)
            smog = (
                (1.043 * (30 * (poly_syllables / sentences)) ** .5)
                + 3.1291)
            return smog
        except ZeroDivisionError:
            return 0.0
    else:
        return 0.0


def coleman_liau_index(text: str):
    letters = pool.chars_per_word(text) * 100
    sentences = pool.words_per_sentence(text) * 100
    coleman = float((0.058 * letters) - (0.296 * sentences) - 15.8)
    return coleman


def automated_readability_index(text: str):
    chrs = len(text)
    words = len(pool.tokenize_words(text))
    sentences = len(pool.sent_tokenize(text))
    try:
        a = float(chrs) / float(words)
        b = float(words) / float(sentences)
        readability = (
            (4.71 * a)
            + (0.5 * b)
            - 21.43)
        return readability
    except ZeroDivisionError:
        return 0.0


def linsear_write_formula(text: str):
    easy_word = 0
    difficult_word = 0
    text_list = text.split()[:100]

    for word in text_list:
        if pool.syllabes_per_word(word) < 3:
            easy_word += 1
        else:
            difficult_word += 1

    text = ' '.join(text_list)

    number = float(
        (easy_word * 1 + difficult_word * 3)
        / len(pool.sent_tokenize(text)))

    if number <= 20:
        number -= 2

    return number / 2


def lix(text: str):
    words = text.split()

    words_len = len(words)
    long_words = len([wrd for wrd in words if len(wrd) > 6])

    per_long_words = (float(long_words) * 100) / words_len
    asl = pool.words_per_sentence(text)
    lix = asl + per_long_words

    return lix[0]


def rix(text: str):
    """
    A Rix ratio is simply the number of long words divided by
    the number of assessed sentences.
    rix = LW/S
    """
    words = text.split()
    long_words_count = len([wrd for wrd in words if len(wrd) > 6])
    sentences_count = len(pool.sent_tokenize(text))

    try:
        rix = long_words_count / sentences_count
    except ZeroDivisionError:
        rix = 0.00

    return rix


FEATURES = [
    RDFRE,
    RDFKGL,
    RDL2
]
