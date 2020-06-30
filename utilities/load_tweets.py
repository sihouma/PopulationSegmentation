#!/usr/bin/env python
# -*- coding: utf-8

# Import Required Libraries
import os
import json
import xml.etree.ElementTree as ET


# Upload tweets from XML
def load_tweets_xml(filename):
    tweets, ids = [], []
    with open(filename, 'r') as filename:
        """read the xml and add the tweet in our tweet arrangement"""
        count = 0
        tree = ET.parse(filename)
        root = tree.getroot()
        for document in root.iter('document'):
            txt = document.text
            txt = txt.replace("![CDATA[", '')
            txt = txt.replace("]]", '')
            txt = txt.strip()
            tweets.append(document.text)
            ids.append(count)
            count += 1
    return tweets, ids


# Load tweets from xml files (pan15)
def load_tweets(DIR, mix=True):
    tweets, ids = [], []
    for root, dirs, files in os.walk(DIR):
        for filename in files:
            if filename.endswith('.xml'):
                tweets_, ids_ = load_tweets_xml(os.path.join(DIR, filename))
                id_user = os.path.basename(filename[:-4])
                tweets.append(tweets_)
                ids.append([(i, id_user) for i in ids_])

    # Return tweets as a dictionary of userid: [tweet1, tweet2,..,tweetn]
    if mix:
        tweets_ = {}
        order_ = []
        for i, id_user in enumerate(ids):
            tweets_[id_user[0][1]] = tweets[i]
            order_.append(id_user[0][1])
        tweets = tweets_
        #tweets = [" ".join(tweets_[id_user]) for id_user in order_]
        ids = order_

    return tweets, ids
