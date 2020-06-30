#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function
import argparse
import codecs
#import cPickle as pickle
import numpy as np
import os

from utilities.load_tweets import load_tweets

NAME = 'ef_list_emoticons'
prefix = 'list_emoticons'

if __name__ == "__main__":
    # Command Line Options
    p = argparse.ArgumentParser(NAME)

    p.add_argument("DIR", default=None,
                   action="store", help="Directory with corpus")

    p.add_argument("LIST1", default=None,
                   action="store", help="File with list of emoticons")

    p.add_argument("-d", "--dir",
                   action="store", dest="dir", default="feats",
                   help="Default directory for features [feats]")

    p.add_argument("-p", "--pref",
                   action="store", dest="pref", default=prefix,
                   help="Prefix to save the file of features %s" % prefix)

    p.add_argument("--mix",
                   action="store_true", dest="mix", default=True,
                   help="Mix tweets into pefiles")

    p.add_argument("-v", "--verbose",
                   action="store_true", dest="verbose",
                   help="Verbose mode [Off]")

    p.add_argument("--stopwords", default=None,
                   action="store", dest="stopwords",
                   help="List of stop words [data/stop_words/stop_words_en.txt]")

    opts = p.parse_args()

    if opts.verbose:
        def verbose(*args):
            print(*args)
    else:
        verbose = lambda *a: None

        # load the tweets and their authors (idtweet and idusers)
    tweets, ids = load_tweets(opts.DIR, mix=opts.mix)

    # Print few information about the tweets
    if opts.verbose:
        for i, tweet in enumerate(tweets[:10]):
            verbose('Tweet example', i + 1, tweet[:100])
        verbose("Total tweets   : ", len(tweets))
        try:
            verbose("Total usres/authors : ", len(set([id for x, id in ids])))
        except ValueError:
            verbose("Total usres/authors : ", len(ids))

    # Compute features

    list_of_words1 = [line.strip() for line in codecs.open(opts.LIST1, encoding='utf-8') if
                      len(line.strip()) > 0]

    counts = []
    for usuario in tweets:
        usuario = usuario.split()
        vec1 = [usuario.count(item) for item in list_of_words1]
        vec = vec1
        counts.append(vec)

    # - We count the words in the tweets
    feats = np.asarray(counts)

    # Save the feature matrix
    #with open(os.path.join(opts.dir, opts.pref + '.dat'), 'wb') as idxf:
        #pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    # print featres matrix information
    verbose("Total features/colums :", feats.shape[1])
    verbose("Total rows:", feats.shape[0])

    # Save the indices by lines of the matrix (tweet, authors)
    #with open(os.path.join(opts.dir, opts.pref + '.idx'), 'wb') as idxf:
        #pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)