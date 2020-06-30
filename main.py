#!/usr/bin/python
from utilities.parser_xml import parse, json_name
from sys import argv
import pandas as pd
import numpy as np

from utilities.load_tweets import load_tweets
from utilities.clean_tweets import clean_tweets

# import the huggingface transformers library so we can load our deep learning NLP model.

import torch
import transformers as ppb
import warnings

warnings.filterwarnings('ignore')

if len(argv) < 2:
    raise Exception("Specify the path of the dataset")

script, path = argv

tweets, user_ids = load_tweets(path)

for user, tweet in tweets.items():
    list_tweets = tweets[user]
    for idx, text in enumerate(list_tweets):
        list_tweets[idx] = clean_tweets(text)
    tweets[user] = list_tweets

df_tweets = pd.DataFrame.from_dict(tweets, orient='index').transpose()

# loading the pre-trained BERT model

# # For DistilBERT:
# model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')
#
# #model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-cased')
# tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
# model = model_class.from_pretrained(pretrained_weights)
#
# users_features_vector = {}
#
# for user_id in df_tweets:
#
#     ## Step1: Tokenization
#     tokenized = df_tweets[user_id].dropna().apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))
#
#     ## Setp2: Padding
#     max_len = 0
#
#     for i in tokenized.values:
#         if len(i) > max_len:
#             max_len = len(i)
#
#     padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])
#
#     ## Step3: Masking
#
#     attention_mask = np.where(padded != 0, 1, 0)
#
#     ##################
#     # Use DistilBert to embed all the tweets
#     ##################
#
#     input_ids = torch.tensor(padded)
#     attention_mask = torch.tensor(attention_mask)
#
#     with torch.no_grad():
#         last_hidden_states = model(input_ids, attention_mask=attention_mask)
#
#     features = last_hidden_states[0][:, 0, :].numpy()
#     user_tweets_vector = features.mean(axis=0)
#     users_features_vector[user_id] = user_tweets_vector


#users_feature = pd.read_csv("/Users/sromdhani/VeevaDataScientist/projects/populationsegmentation/data/users_embeddings.csv", index_col=False, header= None)
#users_features = pd.DataFrame.from_dict(users_features_vector, orient='index')
#users_features.to_csv('/Users/sromdhani/VeevaDataScientist/projects/populationsegmentation/data/users_embeddings.csv', index=True, header=False)

## Clustering

print('done')