import numpy as np
import pandas as pd
import itertools
from scipy import misc
from nltk.corpus import stopwords
import torch
from transformers import BertTokenizer, BertModel
import json
import sys

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
bert_model = BertModel.from_pretrained('bert-base-uncased')
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

# tokenize the dataset. encode_plus pads the data to length 512 and adds a masking list
# as well as an attention list, but it seems like those are actually only necesary for
# using Bert as a model. We're just using it as a feature extractor, so we only need the
# encodings.
def bert_tokenize(speeches):
    dataset = []
    for i, speech in enumerate(speeches, 0):
        pp = []
        for sent in speech:
            """sent = tokenizer.encode_plus(
                        sent,
                        add_special_tokens=True,
                        max_length=512, # Max length BERT can handle.
                        pad_to_max_length=True,
                        return_attention_mask=True
                    )"""
            sent = tokenizer.encode(sent, add_special_tokens=True)
            pp.append(sent)
        dataset.append(pp)
    return dataset

# ---- Example of how to use the preprocessing code. -----
readname = sys.argv[1]

# Load the training data from csv
xtrain, ytrain = load_csv(readname)

# Reduce teh dataset by separating tokens, removing stopwords, and splitting
# speeches into sentences.
xtrain = clean(xtrain)

# Convert 2d array of tokens to a 2d array of bert encodings (which are vocab indexes)
token_set = bert_tokenize(xtrain)

'''print(len(token_set))'''

# Get the first sentence in the first training example and convert it to a tensor
test = torch.tensor(token_set[0][0]).unsqueeze(0)

# The model needs to be in eval mode to avoid dropouts being added
bert_model.eval()
out, hidden = bert_model(test)
# The final hidden state represents the entire sentence (could be interesting to use).
# 'out' is the word-by-word matrix of feature vectors (sentence_len x 768)
print(out.shape, hidden.shape)
