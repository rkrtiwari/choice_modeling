# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 10:00:44 2017

@author: tiwarir
"""

import os
import pandas as pd
import numpy as np
import data_parsing_version_0 as dp
reload(dp)

# set the working directory
os.getcwd()
os.chdir("C:\\Users\\tiwarir\\Documents\\behavior_learning\\python_code")

# Sunteck city data



def determine_starting_col_name(mode = 'MRT', congestion_level = 2):
    if mode == 'MRT':
        if congestion_level == 1:
            return 'Q20'
        if  congestion_level == 2:
            return  'Q14'
    if mode == 'BUS':
        if congestion_level == 1:
            return 'Q32'
        if  congestion_level == 2:
            return  'Q26'
    return  'Invalid Option'

def determine_col_locations(survey_data, start_col_name = 'Q14'):
    start_col = survey_data.columns.get_loc(start_col_name)
    incentive_level_0_q = start_col
    incentive_level_0_a = range(start_col+1 , start_col+7)
    incentive_level_1_q = start_col + 7
    incentive_level_1_a = range(start_col+8, start_col+12)
    incentive_level_2_q = start_col + 12
    incentive_level_2_a = range(start_col+13, start_col+15)
    return incentive_level_0_q, incentive_level_0_a, incentive_level_1_q, incentive_level_1_a, incentive_level_2_q, incentive_level_2_a 


def parse_user_response(survey_data, col_locations):
    response = {}
    for i in range(200):
        user_id = int(survey_data['case.no'].iloc[i])
        response[user_id] = {}
        ans_0 = survey_data.iloc[i, col_locations[0]]
        if (ans_0 == 2):       
            dwell_status = 'stay_incentive_level_0'        
            response[user_id]['dwell_status'] = dwell_status
            response[user_id]['dwell_time_hr_inc_0'] = survey_data.iloc[i, col_locations[1][0]]
            response[user_id]['dwell_time_hr_inc_1'] = survey_data.iloc[i, col_locations[1][1]]
            response[user_id]['dwell_time_hr_inc_2'] = survey_data.iloc[i, col_locations[1][2]]
            response[user_id]['dwell_time_min_inc_0'] = survey_data.iloc[i, col_locations[1][3]]
            response[user_id]['dwell_time_min_inc_1'] = survey_data.iloc[i, col_locations[1][4]]
            response[user_id]['dwell_time_min_inc_2'] = survey_data.iloc[i, col_locations[1][5]]
            response[user_id]['dwell_time_inc_0'] = 60*response[user_id]['dwell_time_hr_inc_0'] + response[user_id]['dwell_time_min_inc_0']
            response[user_id]['dwell_time_inc_1'] = 60*response[user_id]['dwell_time_hr_inc_1'] + response[user_id]['dwell_time_min_inc_1']
            response[user_id]['dwell_time_inc_2'] = 60*response[user_id]['dwell_time_hr_inc_2'] + response[user_id]['dwell_time_min_inc_2']
        if (ans_0 == 1):
            ans_1 = survey_data.iloc[i, col_locations[2]]
            if(ans_1 == 2):
                dwell_status = 'stay_incentive_level_1'
                response[user_id]['dwell_status'] = dwell_status
                response[user_id]['dwell_time_hr_inc_1'] = survey_data.iloc[i, col_locations[3][0]]
                response[user_id]['dwell_time_hr_inc_2'] = survey_data.iloc[i, col_locations[3][1]]
                response[user_id]['dwell_time_min_inc_1'] = survey_data.iloc[i, col_locations[3][2]]
                response[user_id]['dwell_time_min_inc_2'] = survey_data.iloc[i, col_locations[3][3]]
                response[user_id]['dwell_time_inc_1'] = 60*response[user_id]['dwell_time_hr_inc_1'] + response[user_id]['dwell_time_min_inc_1']
                response[user_id]['dwell_time_inc_2'] = 60*response[user_id]['dwell_time_hr_inc_2'] + response[user_id]['dwell_time_min_inc_2']
            if(ans_1 == 1):
                ans_2 = survey_data.iloc[i, col_locations[4]]
                if(ans_2 == 2):
                    dwell_status = 'stay_incentive_level_2'
                    response[user_id]['dwell_status'] = dwell_status
                    response[user_id]['dwell_time_hr'] = survey_data.iloc[i, col_locations[5][0]]
                    response[user_id]['dwell_time_min'] = survey_data.iloc[i, col_locations[5][1]]
                    response[user_id]['dwell_time'] = 60*response[user_id]['dwell_time_hr'] + response[user_id]['dwell_time_min']
                if(ans_2 == 1):
                    dwell_status = 'do not stay'
                    response[user_id]['dwell_status'] = dwell_status
    return response

def parse_user_info(survey_data):
    user_info = {}
    for i in range(200):
        id = int(survey_data['case.no'].iloc[i])
        user_info[id] = {}
        if survey_data.Q52.iloc[i] == 1:
            user_info[id]['gender'] = 1
        if survey_data.Q52.iloc[i] == 2:
            user_info[id]['gender'] = 2
    return user_info

def determine_incentive_values(congestion_level = 2):
    incentive_0 = 0
    if congestion_level == 1:
        incentive_1 = 3
        incentive_2 = 7
        
    if congestion_level == 2:
        incentive_1 = 5
        incentive_2 = 10
        
    return incentive_0, incentive_1, incentive_2
    

def create_user_choice_df(user_response, user_info, mode, congestion_level):
    choice_data = pd.DataFrame(columns = ('user', 'gender', 'decision', 'mode', 'congestion_level', 'incentive', 'dwell_time'))
    
    incentive = determine_incentive_values(congestion_level)
    
    j = 0
    for i in range(1,200):
        if 'dwell_status' in user_response[i]:
            gender = user_info[i]['gender']
            if user_response[i]['dwell_status'] == 'do not stay':
                dwell_time = 0
                choice_data.loc[j] = [i, gender, 1, mode, congestion_level, incentive[0], dwell_time]
                j = j+1
                
            if user_response[i]['dwell_status'] == 'stay_incentive_level_0':
                dwell_time_inc_0 = user_response[i]['dwell_time_inc_0']
                choice_data.loc[j] = [i, gender, 1, mode, congestion_level, incentive[0], dwell_time_inc_0]
                j = j+1 
                
                dwell_time_inc_1 = user_response[i]['dwell_time_inc_1']
                choice_data.loc[j] = [i, gender, 1, mode, congestion_level, incentive[1], dwell_time_inc_1]
                j = j+1     
                
                
                dwell_time_inc_2 = user_response[i]['dwell_time_inc_2']
                choice_data.loc[j] = [i, gender, 1, mode, congestion_level, incentive[2], dwell_time_inc_2]
                j = j+1   
                
            if user_response[i]['dwell_status'] == 'stay_incentive_level_1':            
                dwell_time_inc_1 = user_response[i]['dwell_time_inc_1']
                choice_data.loc[j] = [i, gender, 1, mode, congestion_level, incentive[1], dwell_time_inc_1]
                j = j+1     
                
                dwell_time_inc_2 = user_response[i]['dwell_time_inc_2']
                choice_data.loc[j] = [i, gender, 1, mode, congestion_level, incentive[2], dwell_time_inc_2]
                j = j+1 
                
            if user_response[i]['dwell_status'] == 'stay_incentive_level_2':            
                dwell_time_inc_2 = user_response[i]['dwell_time']
                choice_data.loc[j] = [i, gender, 1, mode, congestion_level, incentive[2], dwell_time_inc_2]
                j = j+1 
                
    return choice_data

def compare_old_and_new_result(choice_data_new, choice_data_old):
    i = np.random.choice(range(167))
    col_names = ['user', 'decision', 'incentive', 'dwell_time']
    print  choice_data_new.loc[i,col_names]
    print choice_data_old.loc[i, col_names]
    return


if __name__ == '__main__':
    survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)
    mode = 'MRT'   #options 'Bus', 'MRT'
    congestion_level = 2   #options 1, 2
    start_col_name =  determine_starting_col_name(mode, congestion_level)
    col_locations = determine_col_locations(survey_data, start_col_name)
    user_response = parse_user_response(survey_data, col_locations)
    user_info = parse_user_info(survey_data)
    incentive_value = determine_incentive_values(congestion_level)
    choice_data_new = create_user_choice_df(user_response, user_info, mode, congestion_level)
    choice_data_old = dp.parse_user_response(survey_data)
    compare_old_and_new_result(choice_data_new, choice_data_old)
    
    
    
    