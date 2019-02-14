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
    
    need separation rule of FOMC1 and FOMC2 from separation.xlsx
    
    This function writes the tokenized documents in raw_token.xlsx, which includes columns of 
    
    Date: date of the meeting
    Section: FOMC1 or FOMC2
    Speaker: speaker of the interjection
    content: list of tokens in the interjection
    
    '''
    
    separation = pd.read_excel('separation.xlsx')
    
    text = pd.read_excel('raw_text.xlsx')
    text = text.fillna('0')
    date = text['Date'].unique()
    speaker = []
    document = []
    for meeting_date in date:
        meeting_text = list(text[text['Date'] == meeting_date]['content'].values)
        speaker_list = list(text[text['Date'] == meeting_date]['Speaker'].values)
        document.append(meeting_text)
        speaker.append(speaker_list)
    
    text['content'] = tokenize(text['content'].values)
    text.to_excel('FOMC_token_all.xlsx')
    
    FOMC1_content, FOMC2_content, FOMC1_speaker, FOMC2_speaker = separation_func(document, speaker, separation)
#    FOMC1_speaker, FOMC1_content = separate_speaker(FOMC1)
#    FOMC2_speaker, FOMC2_content = separate_speaker(FOMC2)
    FOMC1_token = tokenize_doc(FOMC1_content)
    FOMC2_token = tokenize_doc(FOMC2_content)
    final = final_merge(FOMC1_token, FOMC1_speaker, FOMC2_token, FOMC2_speaker, date)
    final.to_excel('FOMC_token_separated.xlsx')    
        

        
def separation_func(document, speaker, separation):
    
    '''
    separate documents based on FOMC1 and FOMC2 separation
    
    input: 
    document (list of words): list of 150 meetings, each meeting is a list of all interjections
    speaker: list of 150 meetings, each meeting is a list of all speakers in the meeting
    separation: separation rule of the documents
    
    return: 
    
    FOMC1: list of 150 FOMC1 sections
    FOMC2: list of 150 FOMC2 sections
    FOMC1_speaker: list of the corresponding speakers of FOMC1 sections
    FOMC2_speaker: list of corresponding speakers of FOMC2 sections
    
    '''
    FOMC1 = []
    FOMC2 = []
    FOMC1_speaker = []
    FOMC2_speaker = []
    
    for (i,meeting) in enumerate(document):
        try:
            FOMC1.append(meeting[int(separation['FOMC1'][i]):int(separation['FOMC2'][i])])
            FOMC2.append(meeting[int(separation['FOMC2'][i]):])
            
            FOMC1_speaker.append(speaker[i][int(separation['FOMC1'][i]):int(separation['FOMC2'][i])])
            FOMC2_speaker.append(speaker[i][int(separation['FOMC2'][i]):])
        except TypeError:
            pass

    return FOMC1, FOMC2, FOMC1_speaker, FOMC2_speaker        

def tokenize_doc(content):
    
    '''
    tokenize the content. 
    1. remove all words with length of 1
    2. remove all non-alphabetical words
    3. remove all stop-words
    4. stem all the remaining words
    
    input: content: list of list of words
    
    return: the corresponding tokenized lists
    '''
    FOMC_token = []
    for meeting in content:
        meeting_token = []
        for statement in meeting:
            docsobj = topicmodels.RawDocs([statement], "long")
            docsobj.token_clean(1)
            docsobj.stopword_remove("tokens")
            docsobj.stem()
            docsobj.stopword_remove("stems")
            ps = PorterStemmer()
            meeting_token.append(' '.join([ps.stem(word) for word in docsobj.tokens[0]]))
        FOMC_token.append(meeting_token)
        
    return FOMC_token


def final_merge(FOMC1_token, speaker_FOMC1, FOMC2_token, speaker_FOMC2, date):
    
    '''
    
    merge all results in one dataframe
    
    input: 
        FOMC2_token: tokenized FOMC1 data
        FOMC2_token: tokenized FOMC2 data
        speaker_FOMC1: speakers in each FOMC1 sections
        speaker_FOMC2: speaker in each FOMC2 sections
        date: list of dates of meetings
        
    output: 
        dataframe containing the meeting date, section of the interjection, speaker of the interjection, and the tokenized
        interjection content. 
        
    '''
    df_all = pd.DataFrame(columns = ['Meeting','Section','Speaker','Content'])
    for i in np.arange(len(FOMC1_token)):
        df1 = pd.DataFrame(columns = ['Meeting','Section','Speaker','Content'])
        df1['Speaker'] = speaker_FOMC1[i]
        df1['Content'] = FOMC1_token[i]
        df1['Meeting'] = date[i]
        df1['Section'] = 'FOMC1'
        df_all = df_all.append(df1, ignore_index = True)
        df2 = pd.DataFrame(columns = ['Meeting','Section','Speaker','Content'])
        df2['Speaker'] = speaker_FOMC2[i]
        df2['Content'] = FOMC2_token[i]
        df2['Meeting'] = date[i]
        df2['Section'] = 'FOMC2'  
        df_all = df_all.append(df2, ignore_index = True)
        
    return df_all
    

def tokenize(content):
    
    FOMC_token = []
    for statement in content:
        docsobj = topicmodels.RawDocs([statement], "long")
        docsobj.token_clean(1)
        docsobj.stopword_remove("tokens")
        docsobj.stem()
        docsobj.stopword_remove("stems")
        ps = PorterStemmer()
        FOMC_token.append(' '.join([ps.stem(word) for word in docsobj.tokens[0]]))
        
    return FOMC_token