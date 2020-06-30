#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

#import cPickle as pickle
import numpy as np
import pandas as pd
import argparse
import os
import codecs

# Local imports
from utilities.load_tweets import load_tweets

# Config Variable
NAME = 'ef_tfidf'
prefix = 'tfidf'

if __name__ == "__main__":
    # Commande Line Options
    p = argparse.ArgumentParser(NAME)
    p.add_argument("DIR", default=None,
                   action="store", help="Directory with corpus with json")
    p.add_argument("-d", "--dir",
                   action="store", dest="dir", default="feats",
                   help="Default directory for features [feats]")
    p.add_argument("-p", "--pref",
                   action="store_true", dest="pref", default=prefix,
                   help="Prefix to save the file of features %s" % prefix)
    p.add_argument("--vect",
                   action="store", dest="vect", default=None,
                   help="Training vector file")
    p.add_argument("--mix",
                   action="store_true", dest="mix", default=True,
                   help="Mix tweets into pefiles")
    p.add_argument("--stopwords", default=None,
                   action="store", dest="stopwords",
                   help="List of stop words [data/stopwords.txt]")
    p.add_argument("--ngram",
                   action="store", dest="ngrammax", default=1, type=int,
                   help="El valor máximo de ngramas ")
    p.add_argument("--min",
                   action="store", dest="min", default=10, type=int,
                   help="Define el valor minimo de cuentas ")
    p.add_argument("-v", "--verbose",
                   action="store_true", dest="verbose",
                   help="Verbose mode [Off]")
    opts = p.parse_args()

    # preoare verbose function
    if opts.verbose:
        def verbose(*args):
            print(*args)
    else:
        verbose = lambda *a: None

    # collect the tweets and their authors (idtweet y idusers)
    tweets, ids = load_tweets(opts.DIR, mix=opts.mix)

    # print some info about the tweets
    if opts.verbose:
        for i, tweet in enumerate(tweets[:10]):
            verbose('Tweet example', i + 1, tweet[:100])
        verbose("Total tweets   : ", len(tweets))
        try:
            verbose("Total usuarios : ", len(set([id for x, id in ids])))
        except ValueError:
            verbose("Total usuarios : ", len(ids))

    # Calculate features
    # Get the list of Stop Words
    if not opts.stopwords:
        my_stop_words = []
    else:
        from sklearn.feature_extraction import text
        my_stop_words = text.ENGLISH_STOP_WORDS

    # - Create the counter
    if not opts.vect:
        from sklearn.feature_extraction.text import TfidfVectorizer

        tfidf_vect = TfidfVectorizer(min_df=opts.min,
                                     stop_words=set(my_stop_words),
                                     ngram_range=(1, opts.ngrammax))
        # - count the word frequencies in the tweets
        feats = tfidf_vect.fit_transform(np.asarray(tweets))
    else:
        with open(opts.vect, "r") as model:
            s = model.read()
            #tfidf_vect = pickle.loads(s)
            # - count the word frequencies in the tweets
            #feats = tfidf_vect.transform(np.asarray(tweets))

    # Save the features matrix
    #with open(os.path.join(opts.dir, prefix + '.dat'), 'wb') as idxf:
        #pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    #with open(os.path.join(opts.dir, prefix + '.vec'), 'wb') as idxf:
        #pickle.dump(tfidf_vect, idxf, pickle.HIGHEST_PROTOCOL)

    dense = feats.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=tfidf_vect.get_feature_names())

    # print son features info
    verbose("First 10 features names :", tfidf_vect.get_feature_names()[:10])
    verbose("Total number of features :", feats.shape[1])
    verbose("Total nuber of rows:", feats.shape[0])

    # Save the indexes by rows of the matrix (user or tweet, user)
    #with open(os.path.join(opts.dir, prefix + '.idx'), 'wb') as idxf:
        #pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)