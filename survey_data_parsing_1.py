# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 12:57:09 2017

@author: tiwarir
"""

import os
import pandas as pd
#import numpy as np
#import data_parsing_version_0 as dp
#reload(dp)

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
        user_id = int(survey_data['case.no'].iat[i])
        user_gender = survey_data.Q52.iat[i]
        response[user_id] = {}
        response[user_id]['gender'] = user_gender
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
                    response[user_id]['dwell_time_hr_inc_2'] = survey_data.iloc[i, col_locations[5][0]]
                    response[user_id]['dwell_time_min_inc_2'] = survey_data.iloc[i, col_locations[5][1]]
                    response[user_id]['dwell_time_inc_2'] = 60*response[user_id]['dwell_time_hr_inc_2'] + response[user_id]['dwell_time_min_inc_2']
                if(ans_2 == 1):
                    dwell_status = 'do not stay'
                    response[user_id]['dwell_status'] = dwell_status
    return response

def get_parsed_data(survey_data):
    parsed_data = {}
    parsed_data['MRT'] = {}
    parsed_data['BUS'] = {}
    for mode in ['MRT', 'BUS']:
        for congestion_level in [1,2]:
            start_col_name =  determine_starting_col_name(mode, congestion_level)
            col_locations = determine_col_locations(survey_data, start_col_name)
            user_response = parse_user_response(survey_data, col_locations)
            parsed_data[mode][congestion_level] = user_response
    return parsed_data
            
            
#survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)


if __name__ == '__main__':
    os.chdir("C:\\Users\\tiwarir\\Documents\\behavior_learning\\scc_model")
    survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)
    parsed_data = get_parsed_data(survey_data)


            

    