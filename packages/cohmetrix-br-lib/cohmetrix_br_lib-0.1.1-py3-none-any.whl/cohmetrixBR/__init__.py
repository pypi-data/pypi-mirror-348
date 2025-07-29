import nltk
import spacy
import spacy.cli

nltk.download(['punkt', 'rslp'], quiet=True)


for m in ['pt_core_news_md', 'en_core_web_sm']:
    try:
        spacy.load(m)
    except Exception:
        spacy.cli.download(m)


del nltk
del spacy
