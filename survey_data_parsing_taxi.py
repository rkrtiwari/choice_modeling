# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:37:36 2017

@author: tiwarir
"""

import os
import pandas as pd

# general data parsing
def determine_starting_col_name(congestion_level = 2):
    if congestion_level == 2:
        return 'Q38'
    if congestion_level == 1:
        return 'Q41'
    return  'Invalid Option'


def determine_col_locations(survey_data, start_col_name):
    start_col = survey_data.columns.get_loc(start_col_name)
    incentive_level_0_q = start_col
    incentive_level_1_q = start_col + 1
    incentive_level_2_q = start_col + 2
    return incentive_level_0_q, incentive_level_1_q, incentive_level_2_q        
        
def parse_user_response(survey_data, col_locations):
    response = {}
    for i in range(200):
        user_id = int(survey_data['case.no'].iloc[i])
        response[user_id] = {}
        ans_0 = survey_data.iloc[i, col_locations[0]]
        if (ans_0 == 2):       
            dwell_status = 'stay_incentive_level_0'        
            response[user_id]['dwell_status'] = dwell_status
            response[user_id]['dwell_time'] = 60
            response[user_id]['incentive'] = 0
        if (ans_0 == 1):
            ans_1 = survey_data.iloc[i, col_locations[1]]
            if(ans_1 == 2):
                dwell_status = 'stay_incentive_level_1'
                response[user_id]['dwell_status'] = dwell_status
                response[user_id]['dwell_time'] = 60
                response[user_id]['incentive'] = 5
            if(ans_1 == 1):
                ans_2 = survey_data.iloc[i, col_locations[2]]
                if(ans_2 == 2):
                    dwell_status = 'stay_incentive_level_2'
                    response[user_id]['dwell_status'] = dwell_status
                    response[user_id]['dwell_time'] = 60
                    response[user_id]['incentive'] = 10
                if(ans_2 == 1):
                    dwell_status = 'do not stay'
                    response[user_id]['dwell_status'] = dwell_status
                    response[user_id]['dwell_time'] = 0
                    response[user_id]['incentive'] = 0        
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

def create_user_choice_df(user_response, user_info, congestion_level):
    choice_data = pd.DataFrame(columns = ('user', 'gender', 'decision', 'incentive', 'congestion_level','waiting_time_in_q', 'dwell_time'))       
    j = 0
    
    for i in range(1,200):
        if 'dwell_status' in user_response[i]:
            gender = user_info[i]['gender']
            if user_response[i]['dwell_status'] == 'do not stay':
                incentive = 0
                if congestion_level == 1:
                    waiting_time_in_q = 15
                if congestion_level == 2:
                    waiting_time_in_q = 30
                
                dwell_time = 0
                choice_data.loc[j] = [i, gender, 1, incentive, congestion_level, waiting_time_in_q, dwell_time]
                j = j+1
                
            if user_response[i]['dwell_status'] == 'stay_incentive_level_0':
                incentive = 0
                waiting_time_in_q = 0
                dwell_time = 60
                choice_data.loc[j] = [i, gender, 1, incentive, congestion_level, waiting_time_in_q, dwell_time]
                j = j+1
                
            if user_response[i]['dwell_status'] == 'stay_incentive_level_1':            
                incentive = 5
                waiting_time_in_q = 0
                dwell_time = 60
                choice_data.loc[j] = [i, gender, 1, incentive, congestion_level, waiting_time_in_q, dwell_time]
                j = j+1     
               
            if user_response[i]['dwell_status'] == 'stay_incentive_level_2':            
                incentive = 10
                waiting_time_in_q = 0
                dwell_time = 60
                choice_data.loc[j] = [i, gender, 1, incentive, congestion_level, waiting_time_in_q, dwell_time]
                j = j+1
                
    return choice_data






if __name__ == '__main__':
    os.chdir('C:\\Users\\tiwarir\\Documents\\behavior_learning\\final_code')
    os.getcwd()
    pd.set_option('expand_frame_repr', False)
    survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0) 
    for congestion_level in [1,2]:
        filename = "choice_data_%s_cong_%s.csv" %('taxi',congestion_level)
        start_col_name = determine_starting_col_name(congestion_level)
        col_locations = determine_col_locations(survey_data, start_col_name)
        user_response = parse_user_response(survey_data, col_locations)
        user_info = parse_user_info(survey_data)
        choice_data = create_user_choice_df(user_response, user_info, congestion_level)
        print choice_data
        choice_data.to_csv(filename, index = False)
    
################################################################################
## data parsing for congestion level 2
################################################################################
#
#survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)
#choice_data = pd.DataFrame(columns = ('user', 'gender', 'decision', 'incentive', 'congestion_level','waiting_time_in_q', 'dwell_time'))
#j = 0
#
#
#response38 = survey_data.Q38
#for i, response38 in enumerate(survey_data.Q38):
#    uid = survey_data['case.no'].iat[i]
#    gender = survey_data.Q52.iat[i]
#    if response38 == 1:
#        response39 = survey_data.Q39.iat[i]
#        if response39 == 1:
#            response40 = survey_data.Q40.iat[i]
#            if response40 == 1:
#                waiting_time_in_q = 30
#                dwell_time = 0
#                congestion_lvl = 2
#                incentive = 0
#                choice_data.loc[j] = [uid, gender, 1, incentive, congestion_lvl, waiting_time_in_q, dwell_time]
#                j = j+1
#            if response40 == 2:
#                waiting_time_in_q = 0
#                dwell_time = 60
#                congestion_lvl = 0
#                incentive = 10
#                choice_data.loc[j] = [uid, gender, 1, incentive, congestion_lvl, waiting_time_in_q, dwell_time]
#                j = j+1
#        if  response39 == 2:
#            waiting_time_in_q = 0
#            dwell_time = 60
#            congestion_lvl = 0
#            incentive = 5
#            choice_data.loc[j] = [uid, gender, 1, incentive, congestion_lvl, waiting_time_in_q, dwell_time]
#            j = j+1
#    
#    if response38 == 2:
#         waiting_time_in_q = 0
#         dwell_time = 60
#         congestion_lvl = 0
#         incentive = 0
#         choice_data.loc[j] = [uid, gender, 1, incentive, congestion_lvl, waiting_time_in_q, dwell_time]
#         j = j+1
#         
#
################################################################################
## data parsing for congestion level 1
################################################################################         
#survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)
#choice_data = pd.DataFrame(columns = ('user', 'gender', 'decision', 'incentive', 'congestion_level','waiting_time_in_q', 'dwell_time'))
#j = 0
#
#
#response41 = survey_data.Q41
#for i, response41 in enumerate(survey_data.Q41):
#    uid = survey_data['case.no'].iat[i]
#    gender = survey_data.Q52.iat[i]
#    if response41 == 1:
#        response42 = survey_data.Q42.iat[i]
#        if response42 == 1:
#            response43 = survey_data.Q40.iat[i]
#            if response43 == 1:
#                waiting_time_in_q = 15
#                dwell_time = 0
#                congestion_lvl = 1
#                incentive = 0
#                choice_data.loc[j] = [uid, gender, 1, incentive, congestion_lvl, waiting_time_in_q, dwell_time]
#                j = j+1
#            if response43 == 2:
#                waiting_time_in_q = 0
#                dwell_time = 60
#                congestion_lvl = 0
#                incentive = 10
#                choice_data.loc[j] = [uid, gender, 1, incentive, congestion_lvl, waiting_time_in_q, dwell_time]
#                j = j+1
#        if  response42 == 2:
#            waiting_time_in_q = 0
#            dwell_time = 60
#            congestion_lvl = 0
#            incentive = 5
#            choice_data.loc[j] = [uid, gender, 1, incentive, congestion_lvl, waiting_time_in_q, dwell_time]
#            j = j+1
#    
#    if response41 == 2:
#         waiting_time_in_q = 0
#         dwell_time = 60
#         congestion_lvl = 0
#         incentive = 0
#         choice_data.loc[j] = [uid, gender, 1, incentive, congestion_lvl, waiting_time_in_q, dwell_time]
#         j = j+1            
#            
#        
