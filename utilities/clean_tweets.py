import nltk
import re
from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
from collections import Counter
#from spellchecker import SpellChecker
import os

#spell = SpellChecker()


", ".join(stopwords.words('english'))

STOPWORDS = set(stopwords.words('english'))


def clean_tweets(text):
    text = text.lower()
    text = remove_freqwords(text)
    text = remove_rarewords(text)
    text = remove_stopwords(text)
    text = remove_urls(text)
    text = remove_emoji(text)
    text = remove_emoticons(text)
    text = remove_punctuations(text)
    text = text.replace("username", "")
    text = text.replace(" im ", " i am ")
    text = text.replace(" rt ", "")
    text = text.replace(" via ", "")
    text = text.replace(" luv ", " love ")
    return text


def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    url_pattern.sub(r'URL', text)
    return url_pattern.sub(r'', text)


def remove_stopwords(text):
    """custom function to remove the stopwords"""
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])


def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_punctuations(text):

    PUNCT_TO_REMOVE = string.punctuation
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))


def remove_emoticons(text):
    EMOTICONS=[]
    with open(os.path.join('data', 'emoticons.txt'), encoding='utf-8-sig') as f:
        EMOTICONS=[word for line in f for word in line.split()]
    words = [word for word in str(text).split() if word not in EMOTICONS]
    return " ".join(words)


def remove_freqwords(text):
    """custom function to remove the frequent words"""
    cnt = Counter()
    for word in text.split():
        cnt[word] += 1
    cnt.most_common(10)
    FREQWORDS = set([w for (w, wc) in cnt.most_common(10)])
    return " ".join([word for word in str(text).split() if word not in FREQWORDS])


def remove_rarewords(text):
    """custom function to remove the rare words"""
    cnt = Counter()
    n_rare_words = 10
    RAREWORDS = set([w for (w, wc) in cnt.most_common()[:-n_rare_words - 1:-1]])
    return " ".join([word for word in str(text).split() if word not in RAREWORDS])


# def correct_spellings(text):
#     corrected_text = []
#     misspelled_words = spell.unknown(text.split())
#     for word in text.split():
#         if word in misspelled_words:
#             corrected_text.append(spell.correction(word))
#         else:
#             corrected_text.append(word)
#     return " ".join(corrected_text)