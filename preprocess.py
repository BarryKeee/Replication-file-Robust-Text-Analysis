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
    
    separation = pd.read_excel('separation.xlsx')
    
    text = pd.read_excel('raw_text.xlsx')
    date = text['Date'].unique()
    speaker = []
    document = []
    for meeting_date in date:
        meeting_text = list(text[text['Date'] == meeting_date]['content'].values)
        speaker_list = list(text[text['Date'] == meeting_date]['Speaker'].values)
        document.append(meeting_text)
        speaker.append(speaker_list)
    
    
    FOMC1_content, FOMC2_content, FOMC1_speaker, FOMC2_speaker = separation_func(document, speaker, separation)
#    FOMC1_speaker, FOMC1_content = separate_speaker(FOMC1)
#    FOMC2_speaker, FOMC2_content = separate_speaker(FOMC2)
    FOMC1_token = tokenize(FOMC1_content)
    FOMC2_token = tokenize(FOMC2_content)
    final = final_merge(FOMC1_token, FOMC1_speaker, FOMC2_token, FOMC2_speaker, date)
    final['Speaker'] = text['Speaker'].values
    final.to_excel('raw_token.xlsx')    
        

        
def separation_func(document, speaker, separation):
    
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

            
def separate_speaker(FOMC_meeting):
    
    
    speaker = []
    content = []
    for meeting in FOMC_meeting:
        speaker_meeting = []
        content_meeting = []
        for statement in meeting:
            speaker_meeting.append(statement.split('.')[0])
            content_meeting.append(' '.join(statement.split('.')[1:]))
        speaker.append(speaker_meeting)
        content.append(content_meeting)
            
        
    return speaker, content
    
def tokenize(content):
    
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
    