# all preprocessing codes``

from google_trans_new import google_translator
from textblob.sentiments import NaiveBayesAnalyzer
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS as stopwords
from textblob import Word
from textblob import TextBlob
from bs4 import BeautifulSoup
import spacy
import os
import json
import re
import unicodedata
import asyncio
import nltk

fpath = os.path.join(os.path.dirname(__file__), 'data/contractions.json')
contractions = json.load(open(fpath))

nlp = spacy.load('en_core_web_md')


def download_nltk_pkgs():
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('tagsets')
    nltk.download('wordnet')
    nltk.download('words')
    nltk.download('mazent_ne_chunker')
    nltk.download('punkt')


def word_count(text):
    return len(text.split())


def char_count(text):
    return len(re.sub(r'\s', '', text))


def avg_word_len(text):
    return char_count(text)/word_count(text)


def stopwords_count(text):
    temp = len([word for word in text.lower().split() if word in stopwords])
    return temp


def hashtags_count(text):
    return len(re.findall(r'#\w+', text))


def mentions_count(text):
    return len(re.findall(r'@\w+', text))


def numerics_count(element):
    return len(re.findall(r'\b\d+\b', element))


def uppers_count(text):
    temp = len([word for word in text.split() if word.isupper()])
    return temp


def lowers_count(text):
    temp = len([word for word in text.split() if word.islower()])
    return temp


# Preprocessing and Cleaning
def to_lower_case(text):
    return text.lower()


def contraction_to_expansion(text):
    return " ".join([contractions.get(word.lower(), word) for word in text.split()])


def remove_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    return re.sub(pattern, '', text)


def count_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    return len(re.findall(pattern, text))


def remove_urls(text):
    pattern = r'\bhttp://\S+\b|\bhttps://\S+\b|\bwww.\S+\w+\.\w+\b'
    return re.sub(pattern, '', text)


def count_urls(text):
    pattern = r'\bhttp://\S+\b|\bhttps://\S+\b|\bwww.\S+\w+\.\w+\b'
    return len(re.findall(pattern, text))


def remove_retweets(text):
    pattern = r'\bRT @\w+'
    return re.sub(pattern, '', text)


def count_retweets(text):
    pattern = r'\bRT @\w+'
    return len(re.findall(pattern, text))


def rm_html(text):
    return BeautifulSoup(text, 'lxml').get_text()


def rm_accented_chars(text):
    temp = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('utf-8', 'ignore')
    return temp


def rm_special_chars(text):
    pattern = r'[^\w\s]'
    return re.sub(pattern, '', text)


def rm_mentions(text):
    return re.sub(r'@\w+', '', text).strip()


def rm_repeated_chars(text):
    pattern = r'(.)\1+'
    sub = r'\1\1'
    return re.sub(pattern, sub, text)


def rm_stopwords(text):
    temp = ' '.join([word for word in text.split() if word not in stopwords])
    return temp


def lemmatize_noun_verb(text):
    doc = nlp(text)
    tokens = []

    for token in doc:
        if token.pos_ in ['VERB', 'NOUN']:
            tokens.append(token.lemma_)
        else:
            tokens.append(token.text)

    text = ' '.join(tokens)
    pattern = r'\s\.'
    text = re.sub(pattern, '', text)
    text = text.strip().replace('  ', ' ')
    return text


def lemmatize(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])


def rm_common_words(text, common_words):
    return ' '.join([word for word in text.split() if word not in common_words])


def rm_rare_words(text, rare_words):
    return ' '.join([word for word in text.split() if word not in rare_words])


def correct_spelling(text):
    words = []
    for word in text.split():
        w = Word(word)
        words.append(w.correct())

    return ' '.join(words)


def get_noun_phrase(text):
    blob = TextBlob(text)
    return blob.noun_phrases


def n_gram(x, n=2):
    return list(TextBlob(x).ngrams(n))


def singularize(text):
    return ' '.join([word.singularize() if tag in ['NNS'] else word for word, tag in TextBlob(text).tags])


def pluralize(text):
    return ' '.join([word.pluralize() if tag in ['NN'] else word for word, tag in TextBlob(text).tags])


def sentiment_analysis(text):
    return TextBlob(text, analyzer=NaiveBayesAnalyzer()).sentiment.classification


# def translate_text(text, dest='ru'):
#     translator = google_translator()
#     return translator.translate(text, lang_tgt=dest).text


# def detect_lang(text):
#     translator = google_translator()
#     return translator.detect(text)

# # def pronounce(text):
# #     translator = google_translator()
# #     return translator.translate(text, lang_tgt=)
