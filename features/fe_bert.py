#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

# Import required libraries
import numpy as np
import pandas as pd

# import the huggingface transformers library so we can load our deep learning NLP model.
import torch
import transformers as ppb
import warnings

warnings.filterwarnings('ignore')


def get_bert_embeddings(autor_tweets=[]):
    # loading the pre-trained BERT model

    # For DistilBERT:
    model_class, tokenizer_class, pretrained_weights = (
        ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')

    ## Want BERT instead of distilBERT? Uncomment the following line:
    # model_class, tokenizer_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-uncased')

    ######################
    # Load pretrained model/tokenizer
    # the variable model holds a pretrained distilBERT model -- a version of BERT that is smaller, but much faster and requiring a lot less memory.
    #####################

    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)

    ####################
    # Preparing the dataset
    #######################

    ## Step1: Tokenization

    tokenized = autor_tweets.apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))

    ## Setp2: Padding

    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)

    padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])


    ## Step3: Masking

    attention_mask = np.where(padded != 0, 1, 0)

    ##################
    # Use DistilBert to embed all the tweets
    ##################

    input_ids = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)

    features = last_hidden_states[0][:,0,:].numpy()

    return np.mean(features,axis = 0)
