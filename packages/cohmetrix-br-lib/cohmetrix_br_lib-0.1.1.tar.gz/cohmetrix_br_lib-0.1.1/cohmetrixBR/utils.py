"""Utility  module
for CohMetrix-BR.
"""
from __future__ import annotations

import csv
import tempfile
from collections import Counter
from functools import lru_cache
from importlib import resources
from pathlib import Path
from zipfile import ZipFile

import gensim
import nltk
import numpy as np
import pandas as pd
import pyphen
import requests
import spacy
from gensim.models import KeyedVectors
from spacy.tokens import Doc
from tqdm.auto import tqdm
from unidecode import unidecode


class ModelPool:
    """Singleton com pool de funcionalidades
    dependentes em modelos/recursos externos. 

    Toda característica que necessite de um
    modelo deve utilizar esse pool.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Criando nova instância
            instance = super().__new__(cls)
            instance._hyphenation = None
            instance._mrc = None
            instance._mrc_words = None
            instance._cbow_s50 = None
            instance._intentional_verbs = None
            instance._layout_one = None
            instance._wordnet = None
            instance._nlp_pt = spacy.load('pt_core_news_md')
            instance._nlp_en = spacy.load('en_core_web_sm')
            instance._punctuations = list(
                "!\"\#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~")

            # Atualizando instância
            cls._instance = instance

        return cls._instance

    @property
    def hyphenation(self) -> pyphen.Pyphen:
        if self._hyphenation is None:
            self._hyphenation = pyphen.Pyphen(lang='pt')

        return self._hyphenation

    @property
    def MRC(self) -> pd.DataFrame:
        if self._mrc is None:
            with resources.path('cohmetrixBR.resources',
                                'MRC.csv') as path:
                self._mrc = pd.read_csv(path)

        return self._mrc

    @property
    def MRC_words(self) -> list:
        if self._mrc_words is None:
            self._mrc_words = list(self.MRC['word'])

        return self._mrc_words

    @property
    def cbow_s50(self) -> gensim.models.KeyedVectors:
        if self._cbow_s50 is None:
            # Checando se o arquivo já existe
            target = Path(__file__).parent.joinpath('resources',
                                                    'cbow_s50.txt')
            if not target.exists():
                self._download_cbow_s50()

            with resources.path('cohmetrixBR.resources',
                                'cbow_s50.txt') as path:
                self._cbow_s50 = KeyedVectors.load_word2vec_format(str(path))

        return self._cbow_s50

    @property
    def intentional_verbs(self):
        if self._intentional_verbs is None:
            with resources.path('cohmetrixBR.resources',
                                'intentional_verbs.csv') as file:
                with open(file, newline='') as f:
                    reader = csv.reader(f)
                    self._intentional_verbs = [row[0] for row in reader]

        return self._intentional_verbs

    @property
    def layout_one(self):
        if self._layout_one is None:
            with resources.open_text('cohmetrixBR.resources',
                                     'layout-one.txt',
                                     encoding='utf-8',
                                     errors='ignore') as f:
                self._layout_one = f.read().splitlines()

        return self._layout_one

    @property
    def wordnet(self):
        if self._wordnet is None:
            self._wordnet = []
            for line in self.layout_one:
                line = line.replace('[', '').replace(']', '').replace(
                    '{', '').replace('}', '').replace(',', '').split(' ')[1::]

                if line:
                    words = line[1::]

                    for w in words:
                        if '<' in w:
                            words.remove(w)

                    self._wordnet.append(words)

        return self._wordnet

    @lru_cache(8)
    def nlp(self, text: str, lang: str = 'pt') -> Doc:
        if lang == 'pt':
            return self._nlp_pt(text)

        return self._nlp_en(text)

    @lru_cache(8)
    def sent_tokenize(self,
                      text: str):
        return nltk.sent_tokenize(text, 'portuguese')

    @lru_cache(8)
    def word_tokenize(self,
                      text: str):
        return nltk.word_tokenize(text, 'portuguese')

    def pre_processing_keep_stopword_token(self,
                                           text: str,
                                           lang: str = 'pt'):
        text = self.nlp(text, lang)
        tokens = [word.lower_
                  for word in text
                  if not word.is_digit
                  and not word.is_punct
                  and word.pos_ != "SYM"]
        token = " ".join(tokens)
        return unidecode(token)

    def pre_processing_keep_stopword_lemma(self,
                                           text: str,
                                           lang: str = 'pt'):
        text = self.nlp(text, lang)
        tokens = [word.lemma_
                  for word in text
                  if not word.is_digit
                  and word.pos_ != "SYM"
                  and not word.is_punct]
        token = " ".join(tokens)
        return unidecode(token)

    def tokenize_words(self, text: str) -> list:
        tokens = self.word_tokenize(text)
        words = [t for t in tokens
                 if t not in self._punctuations]
        return words

    def phrases_per_paragraph(self, text: str) -> np.ndarray:
        """Quantity of phrases per paragraph."""
        paragraphs = text.split("\n")
        result = [len(self.sent_tokenize(i))
                  for i in paragraphs]
        return np.array(result)

    def words_per_sentence(self, text: str) -> np.ndarray:
        """Counts how many words there are in each sentence"""
        sentences = self.sent_tokenize(text)
        result = [len(self.tokenize_words(sent))
                  for sent in sentences]
        return np.array(result)

    def chars_per_word(self, text: str) -> np.ndarray:
        """Counts how many chars there are in each word"""
        words = self.tokenize_words(text)
        return np.array([len(word) for word in words])

    def word_count(self, text: str, word: str) -> int:
        """Counts how many times word appear in text"""
        palavras = self.tokenize_words(text)
        return palavras.count(word.lower()) + palavras.count(word.capitalize())

    def syllables_per_word(self, word) -> int:
        """Counts how many silabes in a word"""
        syllables = self.hyphenation.inserted(word)
        return len(syllables.split("-"))

    def cosine_similarity(self, vec1: Counter, vec2: Counter):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = np.sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = np.sum([x ** 2 for x in vec1.values()])
        sum2 = np.sum([x ** 2 for x in vec2.values()])
        denominator = np.sqrt(sum1) * np.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return numerator / denominator

    @staticmethod
    def _download_cbow_s50():
        """Realiza o download do zip dessa URL
        para o diretório indicado.
        """
        # URL do NILC com o CBOW_S50
        model = 'cbow_s50.zip'
        url = 'http://143.107.183.175:22980/'
        url += f'download.php?file=embeddings/word2vec/{model}'
        size = int(requests.head(url).headers['Content-Length'])

        # Local de salvamento
        target = Path(__file__).parent.joinpath('resources').absolute()

        # Tamanho dos chunks (~10MB)
        chunk_size = int(1e7)

        # Realizando download
        with requests.get(url,
                          stream=True,
                          allow_redirects=True) as r:
            r.raise_for_status()

            # Criando arquivo temporário para o zip
            with tempfile.NamedTemporaryFile(suffix='.zip') as temp:
                pbar = tqdm(desc=f'cohmetrix-BR: download {model}',
                            unit_divisor=1024,
                            unit='B',
                            unit_scale=True,
                            total=size)

                # Fazendo o download de cada chunk
                for chunk in r.iter_content(chunk_size=chunk_size):
                    temp.write(chunk)
                    pbar.update(len(chunk))

                # Salvando no sistema de arquivos
                with ZipFile(temp, 'r') as zip:
                    zip.extractall(str(target))
