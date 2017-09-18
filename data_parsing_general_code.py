# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 14:09:12 2017

@author: tiwarir
"""

import os
import pandas as pd
import numpy as np

# set the working directory
os.getcwd()
os.chdir("C:\\Users\\tiwarir\\Documents\\behavior_learning\\python_code")

# Sunteck city data
survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx',
  sheetname = 'SCC 5-6 Dec', skiprows = 0)

# column names



start_col_name = 'Q14' # MRT Question, Congestion level 2
start_col_name = 'Q20' # MRT Question, Congestion level 1
start_col_name = 'Q26' # Bus Question, Congestion level 2
start_col_name = 'Q32' # Bus Question, Congestion level 1

start_col = survey_data.columns.get_loc(start_col_name)
incentive_level_0_q = start_col
incentive_level_0_a = range(start_col+1 , start_col+7)
incentive_level_1_q = start_col + 7
incentive_level_1_a = range(start_col+8, start_col+12)
incentive_level_2_q = start_col + 12
incentive_level_2_a = range(start_col+13, start_col+15)

for i, col in enumerate(survey_data.columns):
    if (i in range(start_col,start_col+15)):
        print i, col


response = {}
for i in range(200):
    user_id = int(survey_data['case.no'].iloc[i])
    response[user_id] = {}
    ans_0 = survey_data.iloc[i, incentive_level_0_q]
    if (ans_0 == 2):       
        dwell_status = 'stay_incentive_level_0'        
        response[user_id]['dwell_status'] = dwell_status
        response[user_id]['dwell_time_hr_inc_0'] = survey_data.iloc[i, incentive_level_0_a[0]]
        response[user_id]['dwell_time_hr_inc_1'] = survey_data.iloc[i, incentive_level_0_a[1]]
        response[user_id]['dwell_time_hr_inc_2'] = survey_data.iloc[i, incentive_level_0_a[2]]
        response[user_id]['dwell_time_min_inc_0'] = survey_data.iloc[i, incentive_level_0_a[3]]
        response[user_id]['dwell_time_min_inc_1'] = survey_data.iloc[i, incentive_level_0_a[4]]
        response[user_id]['dwell_time_min_inc_2'] = survey_data.iloc[i, incentive_level_0_a[5]]
        response[user_id]['dwell_time_inc_0'] = 60*response[user_id]['dwell_time_hr_inc_0'] + response[user_id]['dwell_time_min_inc_0']
        response[user_id]['dwell_time_inc_1'] = 60*response[user_id]['dwell_time_hr_inc_1'] + response[user_id]['dwell_time_min_inc_1']
        response[user_id]['dwell_time_inc_2'] = 60*response[user_id]['dwell_time_hr_inc_2'] + response[user_id]['dwell_time_min_inc_2']
    if (ans_0 == 1):
        ans_1 = survey_data.iloc[i, incentive_level_1_q]
        if(ans_1 == 2):
            dwell_status = 'stay_incentive_level_1'
            response[user_id]['dwell_status'] = dwell_status
            response[user_id]['dwell_time_hr_inc_1'] = survey_data.iloc[i, incentive_level_1_a[0]]
            response[user_id]['dwell_time_hr_inc_2'] = survey_data.iloc[i, incentive_level_1_a[1]]
            response[user_id]['dwell_time_min_inc_1'] = survey_data.iloc[i, incentive_level_1_a[2]]
            response[user_id]['dwell_time_min_inc_2'] = survey_data.iloc[i, incentive_level_1_a[3]]
            response[user_id]['dwell_time_inc_1'] = 60*response[user_id]['dwell_time_hr_inc_1'] + response[user_id]['dwell_time_min_inc_1']
            response[user_id]['dwell_time_inc_2'] = 60*response[user_id]['dwell_time_hr_inc_2'] + response[user_id]['dwell_time_min_inc_2']
        if(ans_1 == 1):
            ans_2 = survey_data.iloc[i, incentive_level_2_q]
            if(ans_2 == 2):
                dwell_status = 'stay_incentive_level_2'
                response[user_id]['dwell_status'] = dwell_status
                response[user_id]['dwell_time_hr'] = survey_data.iloc[i, incentive_level_2_a[0]]
                response[user_id]['dwell_time_min'] = survey_data.iloc[i, incentive_level_2_a[1]]
                response[user_id]['dwell_time'] = 60*response[user_id]['dwell_time_hr'] + response[user_id]['dwell_time_min']
            if(ans_2 == 1):
                dwell_status = 'do not stay'
                response[user_id]['dwell_status'] = dwell_status

            

# reproduce the old result
choice_data_general_code = pd.DataFrame(columns = ('user', 'gender', 'decision', 'incentive', 'congestion_level',
  'dwell_time'))
j = 0
response[3]
for i in range(1,200):
    if 'dwell_status' in response[i]:
        print i, response[i]['dwell_status']
        if response[i]['dwell_status'] == 'do not stay':
            incentive = 0
            dwell_time = 0
            choice_data_general_code.loc[j] = [i, 1, 1, 0, 2, dwell_time]
            j = j+1
            
        if response[i]['dwell_status'] == 'stay_incentive_level_0':
            incentive = 0
            dwell_time_inc_0 = response[i]['dwell_time_inc_0']
            choice_data_general_code.loc[j] = [i, 1, 1, incentive, 2, dwell_time_inc_0]
            j = j+1 
            
            incentive = 5
            dwell_time_inc_1 = response[i]['dwell_time_inc_1']
            choice_data_general_code.loc[j] = [i, 1, 1, incentive, 2, dwell_time_inc_1]
            j = j+1     
            
            
            incentive = 10
            dwell_time_inc_2 = response[i]['dwell_time_inc_2']
            choice_data_general_code.loc[j] = [i, 1, 1, incentive, 2, dwell_time_inc_2]
            j = j+1   
            
        if response[i]['dwell_status'] == 'stay_incentive_level_1':            
            incentive = 5
            dwell_time_inc_1 = response[i]['dwell_time_inc_1']
            choice_data_general_code.loc[j] = [i, 1, 1, incentive, 2, dwell_time_inc_1]
            j = j+1     
            
            
            incentive = 10
            dwell_time_inc_2 = response[i]['dwell_time_inc_2']
            choice_data_general_code.loc[j] = [i, 1, 1, incentive, 2, dwell_time_inc_2]
            j = j+1 
            
        if response[i]['dwell_status'] == 'stay_incentive_level_2':            
            incentive = 10
            dwell_time_inc_2 = response[i]['dwell_time']
            choice_data_general_code.loc[j] = [i, 1, 1, incentive, 2, dwell_time_inc_2]
            j = j+1 
            

i = np.random.choice(range(167))
col_names = ['user', 'decision', 'incentive', 'dwell_time']
print  choice_data.loc[i,col_names]
print choice_data_general_code.loc[i, col_names]

    






