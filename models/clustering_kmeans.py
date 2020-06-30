#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

from sys import argv

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

from sklearn.cluster import KMeans, MiniBatchKMeans

from sklearn.feature_extraction import text
from utilities.load_authors_data import load_authors_data
from utilities.clean_tweets import clean_tweets


import pandas as pd

import warnings

warnings.filterwarnings('ignore')

if len(argv) < 2:
    raise Exception("Specify the path of the dataset")

script, path = argv

if __name__ == "__main__":

    authors_data = load_authors_data(path)

    authors_data['tweet_text'] = authors_data['tweets'].apply(lambda x: " ".join(x))

    #authors_data['tweet_text_clean'] = authors_data['tweet_text'].apply(lambda text: clean_tweets(text))

    my_stop_words = text.ENGLISH_STOP_WORDS

    n_features = 10000  # Maximum number of features (dimensions) to extract from text.
    tfidf_vect = TfidfVectorizer(max_df=0.5, max_features=n_features,
                                 min_df=2, stop_words='english',
                                 use_idf=True)

    # TfidfVectorizer(min_df=opts.min,stop_words=set(my_stop_words),ngram_range=(1, opts.ngrammax))

    # - count the word frequencies in the tweets
    feats = tfidf_vect.fit_transform(authors_data['tweet_text'])

    dense = feats.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=tfidf_vect.get_feature_names())

    # print son features info

    print("Total number of features :", feats.shape[1])
    print("Total nuber of rows:", feats.shape[0])

    lsa_n_components = 2  # Preprocess documents with latent semantic analysis for dimentionality reduction
    svd = TruncatedSVD(lsa_n_components)
    lsa = make_pipeline(svd, Normalizer(copy=False))

    # Vectorizer results are normalized, which makes KMeans behave as
    # spherical k-means for better results. Since LSA/SVD results are
    # not normalized, we have to redo the normalization.
    X_lsa = lsa.fit_transform(feats)

    explained_variance = svd.explained_variance_ratio_.sum()
    print("Explained variance of the SVD step: {}%".format(
        int(explained_variance * 100)))

    km = KMeans(n_clusters=2, init='k-means++', max_iter=100, n_init=1,
                verbose=True)

    y_km = km.fit_predict(X_lsa)

    print('Done')



