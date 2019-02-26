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



def read_raw_data():
    
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
    date = [f[4:10] for f in onlyfiles]

    
    start = timeit.default_timer()
    
    raw_text = pd.DataFrame(columns = ['Date','Speaker', 'content'])

    for i,file in enumerate(filelist):
        parsed = parser.from_file(os.path.join(cwd, 'FOMC_pdf',file))
        interjections = re.split('\nMR. |\nMS. |\nCHAIRMAN |\nVICE CHAIRMAN ', parsed['content'])[1:]
        temp_df = pd.DataFrame(columns = ['Date','Speaker','content'])
        
        interjections = [interjection.replace('\n',' ') for interjection in interjections]
        
        temp_df['Speaker'] = [interjection.split('.')[0] for interjection in interjections]
        
        temp_df['content'] = ['.'.join(interjection.split('.')[1:]) for interjection in interjections]

        temp_df['Date'] = date[i]
        raw_text = pd.concat([raw_text, temp_df], ignore_index = True)
    end = timeit.default_timer()
    raw_text.index = raw_text['Date']
    raw_text.to_excel('raw_text.xlsx')
    print("Documents processed. Time: {}".format(end - start))
    
    return raw_text


def generate_separated_raw_data():
    '''
    Generate raw text data and separate based on separation rule
    
    '''
    
    raw_text = read_raw_data()
    
    start = timeit.default_timer()
    separation = pd.read_excel('Separation.xlsx')

    final = pd.DataFrame(columns = ['Date','Section','Speaker','content'])

    for date in separation.index:
        meeting_date = raw_text[raw_text['Date'].astype(int) == date]
        FOMC1 = meeting_date.iloc[separation['FOMC1_start'][date]:separation['FOMC1_end'][date]]
        if separation['FOMC2_end'][date] == 'end':
            FOMC2 = meeting_date.iloc[separation['FOMC2_start'][date]:]
        else:
            FOMC2 = meeting_date.iloc[separation['FOMC2_start'][date]:separation['FOMC2_end'][date]]
        #FOMC2 = meeting_date.iloc[separation['FOMC2_start'][date]:]
        FOMC1['Section'] =1 
        FOMC2['Section'] = 2
        
        final = pd.concat([final, FOMC1], ignore_index = True)    
        final = pd.concat([final, FOMC2], ignore_index = True)

    end = timeit.default_timer()
    final.to_excel('raw_text_separated.xlsx')
    print("Documents processed. Time: {}".format(end - start))

    return final

        

