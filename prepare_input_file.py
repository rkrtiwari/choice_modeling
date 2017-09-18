# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 15:48:15 2017

@author: tiwarir
"""

import numpy as np
import pandas as pd
import os

def choices_user_wants_to_leave(user_df, congestion_level):
    individual = np.repeat(user_df.user.values, 6)
    gender = np.repeat(user_df.gender.values, 6)
    decision = [1,0,1,0,1,0]
    DT = [0,30,0,30,0,30]
    
    if  congestion_level == 1:
        incentive = [0,0,0,3,0,7]
    if congestion_level == 2:
        incentive = [0,0,0,5,0,10]
        
    mode = ['leave', 'stay']*3
    
    d = {'individual': individual, 'decision': decision, 'DT': DT, 
    'incentive': incentive, 'gender': gender, 'mode': mode}
    
    df_c = pd.DataFrame(d)
    
    return df_c
    
def choices_user_wants_to_stay_for_inc_0(user_df, congestion_level):
    individual = np.repeat(user_df.user.values, 2)
    gender = np.repeat(user_df.gender.values, 2)
    decision = [1, 0, 1, 0, 1, 0]
    dwell_time = user_df.dwell_time.values
    DT = [0, dwell_time[0], 0, dwell_time[1], 0, dwell_time[2]]
    
    if  congestion_level == 1:
        incentive = [0,0,0,3,0,7]
    if congestion_level == 2:
        incentive = [0,0,0,5,0,10]
        
    mode = ['leave', 'stay']*3
    
    d = {'individual': individual, 'decision': decision, 'DT': DT, 
    'incentive': incentive, 'gender': gender, 'mode': mode}
    
    df_c = pd.DataFrame(d)
    
    return df_c    

def choices_user_wants_to_stay_for_inc_1(user_df, congestion_level):
    individual = np.repeat(user_df.user.values, 3)
    gender = np.repeat(user_df.gender.values, 3)
    decision = [1, 0, 0, 1, 0, 1]
    dwell_time = user_df.dwell_time.values
    DT = [0, dwell_time[0], 0, dwell_time[0], 0, dwell_time[1]]
    
    if  congestion_level == 1:
        incentive = [0,0,0,3,0,7]
    if congestion_level == 2:
        incentive = [0,0,0,5,0,10]
        
    mode = ['leave', 'stay']*3
    
    d = {'individual': individual, 'decision': decision, 'DT': DT, 
    'incentive': incentive, 'gender': gender, 'mode': mode}
    
    df_c = pd.DataFrame(d)
    
    return df_c  

def choices_user_wants_to_stay_for_inc_2(user_df, congestion_level):
    individual = np.repeat(user_df.user.values, 6)
    gender = np.repeat(user_df.gender.values, 6)
    decision = [1, 0, 1, 0, 0, 1]
    dwell_time = user_df.dwell_time.values
    DT = [0, dwell_time[0], 0, dwell_time[0], 0, dwell_time[0]]
    
    if  congestion_level == 1:
        incentive = [0,0,0,3,0,7]
    if congestion_level == 2:
        incentive = [0,0,0,5,0,10]
        
    mode = ['leave', 'stay']*3
    
    d = {'individual': individual, 'decision': decision, 'DT': DT, 
    'incentive': incentive, 'gender': gender, 'mode': mode}
    
    df_c = pd.DataFrame(d)
    
    return df_c 


def get_user_choice_df(user, choice_data):
    ind = user == choice_data.user
    user_df = choice_data.loc[ind,].copy()
    congestion_level = user_df.congestion_level.iloc[0]
    n_row, _ = user_df.shape
    
    if (n_row == 1):
        if user_df.incentive.iloc[0] == 0:
            df_c = choices_user_wants_to_leave(user_df, congestion_level)
        else:
            df_c = choices_user_wants_to_stay_for_inc_2(user_df, congestion_level)
    
    if (n_row == 2):
        df_c = choices_user_wants_to_stay_for_inc_1(user_df, congestion_level)
    
    if (n_row == 3):
        df_c = choices_user_wants_to_stay_for_inc_0(user_df, congestion_level)
    
    return df_c

def create_choice_df(choice_data):
    users = choice_data.user.unique()
    df = pd.DataFrame(columns = ['individual', 'decision', 'DT', 'incentive', 'gender', 'mode'])
    for user in users:
        df_c = get_user_choice_df(user, choice_data)
        df = pd.concat([df, df_c])
    
    return df
    
if __name__ == '__main__':
    os.chdir("C:\\Users\\tiwarir\\Documents\\behavior_learning\\python_code")
    import data_parsing_version_1 as dp
    survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)
    mode = 'MRT'   #options 'Bus', 'MRT'
    congestion_level = 2   #options 1, 2
    start_col_name =  dp.determine_starting_col_name(mode, congestion_level)
    col_locations = dp.determine_col_locations(survey_data, start_col_name)
    user_response = dp.parse_user_response(survey_data, col_locations)
    user_info = dp.parse_user_info(survey_data)
    incentive_value = dp.determine_incentive_values(congestion_level)
    choice_data = dp.create_user_choice_df(user_response, user_info, mode, congestion_level)
    df = create_choice_df(choice_data)
    
    
    
    



