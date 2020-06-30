import os
import json

def load_stopwords(DIR):
    stop_words=[]
    with open(os.path.join(DIR, 'stop_words/stop_words_en.txt'), encoding='utf-8-sig') as f:
        stop_words=[word for line in f for word in line.split()]
    with open(os.path.join(DIR, 'emoticons.txt'), encoding='utf-8-sig') as f:
        stop_words=stop_words+[word for line in f for word in line.split()]
    with open(os.path.join(DIR, 'punctuation.txt'), encoding='utf-8-sig') as f:
        stop_words=stop_words+[word for line in f for word in line.split()]
    return stop_words
