import numpy as np
import pandas as pd
import itertools
from scipy import misc
from nltk.corpus import stopwords
import torch
from transformers import BertTokenizer
import json
import sys

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
#bert_model = torch.hub.load('huggingface/pytorch-transformers', 'model', 'bert-base-uncased')

stop_words = set(stopwords.words('english'))
stop_words |= set(['', '``', '-', '--'])

def load_csv(path, train=False, ypath=None):
    data = pd.read_csv(path, names=['text', 'party'])
    xs, ys = data['text'], data['party']

    return xs, ys

def max_speech_len(speeches):
  return max([len(sent) for pp in speeches for sent in pp])

# Don't lemmatize because bert uses its own tokenization approach
#
# Speeches are too long for bert to handle, so we break each one down
# into an array of sentences
def clean(df):
    df = df.str.split(' ')
    for i, row in enumerate(df, 0):
        df[i] = [w for w in row if w not in stop_words]

    for i, row in enumerate(df, 0):
        para_arr, sent_arr = [], []
        for w in row:
            if w in ['.', '?', '!']:
                sent_arr.append(w)
                para_arr.append(sent_arr),
                sent_arr = []
            else:
                sent_arr.append(w)
        df[i] = para_arr

    return df

# tokenize the dataset. The json dump for this is ~500M so
# we may want to consider a way to compute on the fly
def bert_tokenize(speeches):
    dataset = []
    for i, speech in enumerate(speeches, 0):
        pp = []
        for sent in speech:
            sent = tokenizer.encode_plus(
                        xtrain[0][0],
                        add_special_tokens=True,
                        max_length=512, # Max length BERT can handle.
                        pad_to_max_length=True,
                        return_attention_mask=True
                    )
            pp.append(sent)
        dataset.append(pp)
    return dataset

# examples
'''readname, writename = sys.argv[1], sys.argv[2]
xtrain, ytrain = load_csv(readname)

xtrain = clean(xtrain)
token_set = bert_tokenize(xtrain)'''
