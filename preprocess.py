# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 21:47:16 2019

@author: barry
"""


import pandas as pd
import topicmodels
import numpy as np
from nltk.stem import PorterStemmer


def preprocess():
    
    
    '''
    main function for preprocessing
        
    This function writes the tokenized documents, which includes columns of 
    
    Date: date of the meeting
    Section: FOMC1 or FOMC2
    Speaker: speaker of the interjection
    content: list of tokens in the interjection
    
    '''
    
    
    text = pd.read_excel('raw_text_separated.xlsx')
    text = text.fillna('0')
    
    text['content'] = tokenize(text['content'].values)
    text.to_excel('FOMC_token_separated.xlsx')
    
def tokenize(content):
    '''
    Code for tokenization:
        1. remove words with length of 1
        2. remove non-alphabetical words
        3. remove stop words
        4. stem all words
    '''
    FOMC_token = []
    for statement in content:
        statement = statement.lower()
        docsobj = topicmodels.RawDocs([statement], "long")
        docsobj.token_clean(1)
        docsobj.stopword_remove("tokens")
        docsobj.stem()
        docsobj.stopword_remove("stems")
        ps = PorterStemmer()
        FOMC_token.append(' '.join([ps.stem(word) for word in docsobj.tokens[0]]))
        
    return FOMC_token