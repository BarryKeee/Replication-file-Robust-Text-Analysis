# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 21:18:59 2019

@author: barry
"""


import pandas as pd
from gensim import corpora


'''
TODO: make sure runnable for any system
delete unncessary loops in generate_raw_data

'''

def generate_term_document():
    
    '''
    This function generates the term-document matrix from data in raw_token.xlsx
    
    It returns the pandas dataframe of the term-document matrix. It also saves it to term_document.xlsx
    
    '''
    data = pd.read_excel('raw_token.xlsx')
        
    document_content = []
    for statement in data['Content'].values:
        try:
            document_content.append(statement.split(' '))
        except AttributeError:
            document_content.append([])
            
    dictionary = corpora.Dictionary(document_content)
    corpus = [dictionary.doc2bow(text) for text in document_content]
    #print(dictionary.token2id)
    
    
    term_document = pd.DataFrame(index = dictionary.token2id.values())
    for i in range(len(corpus)):
        try:
            dist = pd.DataFrame(corpus[i]).set_index(0)
            term_document[i] = dist[1]
        except KeyError:
            term_document[i] = 0
        
        
    term_document = term_document.fillna(0)
    term_document = term_document.transpose()
    term_document = term_document / term_document.sum(axis = 0)
    term_document.to_excel('term_document.xlsx')
    return term_document