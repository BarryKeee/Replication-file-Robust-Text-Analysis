# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 21:20:54 2019

@author: barry
"""

from tika import parser
import re
import timeit
import os
import pandas as pd



def generate_raw_data():
    
    """
    This function generates raw text data from FOMC transcripts
    
    returns a list where each element is the full text within each FOMC meeting
    
    It will take about 4-5 minutes
    """
    
    cwd = os.getcwd()
    base_directory = './FOMC_pdf'
    raw_doc = os.listdir(base_directory)
    filelist = sorted(raw_doc)
    
    onlyfiles = [f for f in os.listdir(base_directory) if os.path.isfile(os.path.join(base_directory, f))]
    date = [f[4:12] for f in onlyfiles]

    
    start = timeit.default_timer()
    
    document = []
    raw_text = pd.DataFrame(columns = ['Date','Speaker', 'content'])

    for i,file in enumerate(filelist):
        parsed = parser.from_file(os.path.join(cwd, 'FOMC_pdf',file))
        interjections = re.split('MR. |MS. |CHAIRMAN |VICE CHAIRMAN ', parsed['content'])[1:]
        temp_df = pd.DataFrame(columns = ['Date','Speaker','content'])
        interjection_new = []
        for interjection in interjections:
            
            temp_temp_df = pd.DataFrame(columns = ['Date','Speaker','content'], index = [0])
            interjection = interjection.replace('\n',' ')
            temp_temp_df['Speaker'] = interjection.split('.')[0]
            temp_temp_df['content'] = '.'.join(interjection.split('.')[1:])
            temp_df = pd.concat([temp_df, temp_temp_df], ignore_index = True)
            interjection_new.append(interjection)
        temp_df['Date'] = date[i]
        document.append(interjection_new)
        raw_text = pd.concat([raw_text, temp_df], ignore_index = True)
    end = timeit.default_timer()
    raw_text.index = raw_text['Date']
    raw_text.to_excel('raw_text.xlsx')
    print("Documents processed. Time: {}".format(end - start))
    
    return document, date

