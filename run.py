# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 21:57:54 2019

@author: barry
"""


''' function to generate raw document files from pdfs'''
from generate_raw_data import generate_raw_data
''' function to process raw documents '''
from preprocess import preprocess
''' function to generate term-document matrix '''
from generate_term_document import generate_term_document



raw_document = generate_raw_data()
tokenized_document = preprocess()
term_document = generate_term_document()