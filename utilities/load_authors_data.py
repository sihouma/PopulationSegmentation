#!/usr/bin/env python
# -*- coding: utf-8

# Import Required Libraries
import pandas as pd
import argparse

from utilities.load_tweets import load_tweets
from utilities.load_traits import load_traits

############
# Load author data: tweets, sex, age, and personality traits
#############


NAME = 'load_authors_data'

def load_authors_data(DIR, mix=True):

    # collect the tweets and their authors (id_tweet and id_users)
    tweets, ids = load_tweets(DIR, mix)
    traits = load_traits(DIR)

    # Create pandas Dataframce
    df_tweets = pd.DataFrame.from_dict(tweets, orient='index', columns=['tweets'])
    df_traits = pd.DataFrame.from_dict(traits, orient='index')

    df_authors = df_traits.join(df_tweets)

    return df_authors


if __name__ =="__main__":
    # Command line Options
    p = argparse.ArgumentParser(NAME)
    p.add_argument("DIR", default=None,
                   action="store", help="Directory with corpus with json")
    p.add_argument("-d", "--dir",
                   action="store", dest="dir", default="feats",
                   help="Default directory for features [feats]")
    p.add_argument("--mix",
            action="store_true", dest="mix",default=True,
        help="Mix tweets into pefiles")
    p.add_argument("-v", "--verbose",
        action="store_true", dest="verbose",
        help="Verbose mode [Off]")

    opts = p.parse_args()

    if opts.verbose:
        def verbose(*args):
            print(*args)
    else:
        verbose = lambda *a: None

    df_authors = load_authors_data(opts.DIR)

    print('DONE')

