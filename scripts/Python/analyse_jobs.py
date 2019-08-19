#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 02:07:14 2019

@author: lorajohns
"""

# LDA for 'bonus words' -> edmonson
# textrank -- top words kinda boring
# lexrank
from bs4 import BeautifulSoup
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import gensim
from gensim.summarization import summarize
from gensim.summarization import keywords
from gensim.summarization.textcleaner import split_sentences
import numpy as np

import requests
import json
import pandas as pd

df = pd.read_csv("indeed.csv")
jobs = np.empty(len(df))
for i in range(len(df)):
    title = df.iloc[i]["jobtitle"]
    text = df.iloc[i]["text"]
    jobs[i] = [title, text]
    

titles = " ".join([t for t in jobs[:,0]])
text = " ".join([j for j in jobs[:,1]])

print("Summary:")
print(summarize(text, word_count=50))
print("Keywords:")
k = keywords(text, words=10, split=True, scores=False, lemmatize=True)
print(k) #pos_filter=(tuple)

sentences = split_sentences(text)
key_sents = []
for sent in sentences:
    for keyword in k:
        if keyword in sent:
            key_sents.append((keyword, sent))
            
#list(set(key_sents))[:6] #NEED TO ACCOUNT FOR SENTENCES WITH MULTIPLE KEYWORDS
key_sents[:6]

from sumy.summarizers.lex_rank import LexRankSummarizer 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
 
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.reduction import ReductionSummarizer


language = "english"
sentence_count = 5
 
parser = PlaintextParser(text, Tokenizer(language))

summarizer = LexRankSummarizer(Stemmer(language))
summarizer.stop_words = get_stop_words(language)

#Summarize the document with sentences
summary = summarizer(parser.document, sentence_count) 
for sentence in summary:
    print(sentence)
    
def summarize(text, summarizer, sentence_count, bonus_words=['MLK, rights'], language='english'):
    summarizer = summarizer(Stemmer(language))
    summarizer.stop_words = get_stop_words(language)
    if isinstance(summarizer, EdmundsonSummarizer):
        summarizer.bonus_words = bonus_words
        summarizer.stigma_words = ['zdfgthdvndadv']
        summarizer.null_words = summarizer.stop_words
    summary = summarizer(PlaintextParser(text, Tokenizer(language)).document, sentence_count)
    return summary

def print_summary(summary):
    for sentence in summary:
        print(sentence)

for summarizer in [LexRankSummarizer, LuhnSummarizer, LsaSummarizer, TextRankSummarizer,
                   EdmundsonSummarizer, SumBasicSummarizer, KLSummarizer, ReductionSummarizer]:
    print('----' + summarizer.__name__ + '----')
    print_summary(summarize(text,
                            summarizer,
                            sentence_count))
    print()