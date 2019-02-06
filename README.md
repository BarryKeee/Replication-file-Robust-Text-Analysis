# Replication-file-Robust-Text-Analysis

This cite contains preprocessing packages for replication of "A Robust Machine Learning Algorithm for Text Analysis". 

Required python packages: pandas, numpy, topicmodels, nltk, tika

To generate term-document matrix from FOMC transcript PDFs, simply run run.py.

Output files: 

raw_text.xlsx: raw documents generated from PDFs

raw_token.xlsx: tokenized documents generated from raw documents. Tokenized to exclude all non-alphabetical terms, terms with only one character, all stop words. Then stem all terms. 

term_document.xlsx: generate term-document matrix from tokenized documents. 

Each document contains the speaker in each meeting, meeting date, meeting section (FOMC1/FOMC2 based on separation rules).
