# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:37:36 2017

@author: tiwarir
"""

import os
import pandas as pd
import numpy as np
 
def create_alternatives(waiting_time, incentive):
    
    dwell_time = 60   
    leave_option = [         0,         0,  waiting_time, 'leave']
    stay_option  = [dwell_time, incentive,             0,  'stay']
    
    return [leave_option, stay_option]


def create_choices_leave(user, gender, waiting_time, incentive):
    mode = 'TAXI'

    alternatives = create_alternatives(waiting_time, incentive)
    leave_option = alternatives[0]
    stay_option  = alternatives[1]
    selected     = [user, gender, mode] + [1] + leave_option
    unselected   = [user, gender, mode] + [0] + stay_option
                   
    return [selected, unselected] 

def create_choices_stay(user, gender, waiting_time, incentive):
    mode = 'TAXI'
    
    alternatives = create_alternatives(waiting_time, incentive)
    leave_option = alternatives[0]
    stay_option  = alternatives[1]
    selected     = [user, gender, mode] + [1] + stay_option
    unselected   = [user, gender, mode] + [0] + leave_option
       
    return [selected, unselected]

def create_choice_for_individual(user, gender, survey_data):
    survey_col_names = ['Q38', 'Q39', 'Q40', 'Q41', 'Q42', 'Q43']
    incentive = [0, 5, 10, 0, 5, 10]
    waiting_time = [30, 30, 30, 15, 15, 15]
    input_df = pd.DataFrame(columns = ['individual', 'gender', 'mode', 'decision', 'dwell_time', 'incentive','waiting_time', 'alt'])
    col_names = ['individual', 'gender', 'mode', 'decision', 'dwell_time', 'incentive','waiting_time', 'alt']
    
    j = user - 1 # later can make it more general
    
    for i, col in enumerate(survey_col_names):
        choice = None
        if survey_data[col].iat[j] == 1:
            choice = create_choices_leave(user, gender, waiting_time[i], incentive[i])
        if survey_data[col].iat[j] == 2:
            choice = create_choices_stay(user, gender, waiting_time[i], incentive[i])
        if choice is not None:
            choice_df = pd.DataFrame(choice, columns = col_names)
            input_df = input_df.append(choice_df)
                
    return input_df

            
def create_r_input_file(survey_data):
    df_input = pd.DataFrame(columns = ['individual', 'gender', 'mode', 'decision', 'dwell_time', 'incentive','waiting_time', 'alt'])
    for i in range(200):
        user = int(survey_data['case.no'].iat[i])
        gender = survey_data['Q52'].iat[i]
        choice_df = create_choice_for_individual(user, gender, survey_data)
        df_input = df_input.append(choice_df)
    nrow, _ = df_input.shape
#    choice_id = np.repeat(range(nrow/2),2)
#    df_input['choice_id'] = choice_id 
    df_input['congestion'] = 0
    return df_input

    
if __name__ == '__main__':
    os.chdir('C:\\Users\\tiwarir\\Documents\\behavior_learning\\scc_model_taxi')
    survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)
    df = create_r_input_file(survey_data)

   
