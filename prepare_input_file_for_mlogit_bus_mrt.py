# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 13:37:42 2017

@author: tiwarir
"""
import pandas as pd
import numpy as np
import survey_data_parsing_bus_mrt as sdpbm
reload(sdpbm)

def create_alternatives(dwell_time, congestion_level, incentive):
    leave_option = [         0,         0,  congestion_level, 'leave']
    stay_option  = [dwell_time, incentive,                 0, 'stay']
    
    return [leave_option, stay_option]
    

def determine_incentive_value(congestion_level, incentive_level):
    
    incentive = 0
    
    if congestion_level == 1:
        if incentive_level == 1:
            incentive = 3
        if incentive_level == 2:
            incentive = 7
            
    if congestion_level == 2:
        if incentive_level == 1:
            incentive = 5
        if incentive_level == 2:
            incentive = 10
    return incentive

def create_choices_leave(parsed_data, user, mode, congestion_level, dwell_time, incentive):
    
    gender  = parsed_data[mode][congestion_level][user]['gender']
    alternatives = create_alternatives(dwell_time, congestion_level, incentive)
    leave_option = alternatives[0]
    stay_option  = alternatives[1]
    selected     = [user, gender, mode] + [1] + leave_option
    unselected   = [user, gender, mode] + [0] + stay_option
                   
    return [selected, unselected]              

def create_choices_stay(parsed_data, user, mode, congestion_level, incentive_level):
    dwell_time = 30
    
    incentive_key = 'dwell_time_inc_%s' %(str(incentive_level))
    incentive = determine_incentive_value(congestion_level, incentive_level)
    user_dwell_time = parsed_data[mode][congestion_level][user][incentive_key]
    gender = parsed_data[mode][congestion_level][user]['gender']
    
    choice = []
    while (dwell_time <= user_dwell_time):
#        print 'dwell_time: %d, user_dwell_time: %d, incentive: %d' %(dwell_time, user_dwell_time, incentive)
        alternatives = create_alternatives(dwell_time, congestion_level, incentive)
        leave_option = alternatives[0]
        stay_option  = alternatives[1]
        selected     = [user, gender, mode] + [1] + stay_option
        unselected   = [user, gender, mode] + [0] + leave_option
#        print selected
#        print unselected
        choice = choice + [selected, unselected]
#        choice = choice.extend([selected, unselected])                     
        dwell_time += 15
        
    return choice
    
    
def choices_lll(parsed_data, user, mode, congestion_level):
    dwell_time = 30
    incentive = determine_incentive_value(congestion_level, 2)
    choices = create_choices_leave(parsed_data, user, mode, congestion_level, dwell_time, incentive)
    return choices
            
def choices_lls(parsed_data, user, mode, congestion_level):
    
    leave_choices = []
    incentive_level = 2
    incentive_key = 'dwell_time_inc_%s' %(str(incentive_level))
    dwell_time = parsed_data[mode][congestion_level][user][incentive_key]
    for incentive_level in range(0,2):
        incentive = determine_incentive_value(congestion_level, incentive_level)
        leave_choice = create_choices_leave(parsed_data, user, mode, congestion_level, dwell_time, incentive)
        leave_choices.extend(leave_choice)
            
    stay_choices = []
    for  incentive_level in range(2,3):
        stay_choice  = create_choices_stay(parsed_data, user, mode, congestion_level, incentive_level)
        stay_choices.extend(stay_choice)
            
    alt_leave_choices = []
    for incentive_level in range(2,3):
        incentive_key = 'dwell_time_inc_%s' %(str(incentive_level))
        incentive = determine_incentive_value(congestion_level, incentive_level)
        dwell_time = parsed_data[mode][congestion_level][user][incentive_key] + 15
        alt_leave_choice = create_choices_leave(parsed_data, user, mode, congestion_level, dwell_time, incentive)
        alt_leave_choices.extend(alt_leave_choice)
        
    choices = leave_choices + stay_choices + alt_leave_choices   
        
    return choices

def choices_lss(parsed_data, user, mode, congestion_level):
    incentive_level = 1
    incentive_key = 'dwell_time_inc_%s' %(str(incentive_level))
    incentive = determine_incentive_value(congestion_level, 2)
    dwell_time = parsed_data[mode][congestion_level][user][incentive_key]    
    leave_choice = create_choices_leave(parsed_data, user, mode, congestion_level, dwell_time, 0)
#    print 'leave_choice:\n',  leave_choice
    
    stay_choices = []
    for  incentive_level in range(1,3):
        stay_choice  = create_choices_stay(parsed_data, user, mode, congestion_level, incentive_level)
        stay_choices.extend(stay_choice)
#    print 'stay_choices:\n', stay_choices         
        
    alt_leave_choices = []
    for incentive_level in range(1,3):
        incentive_key = 'dwell_time_inc_%s' %(str(incentive_level))
        incentive = determine_incentive_value(congestion_level, incentive_level)
        dwell_time = parsed_data[mode][congestion_level][user][incentive_key] + 15
        alt_leave_choice = create_choices_leave(parsed_data, user, mode, congestion_level, dwell_time, incentive)
        alt_leave_choices.extend(alt_leave_choice)
        
    choices = leave_choice + stay_choices + alt_leave_choices   
            
    return choices
    
def choices_sss(parsed_data, user, mode, congestion_level):
    stay_choices = []
    for  incentive_level in range(0,3):
        stay_choice  = create_choices_stay(parsed_data, user, mode, congestion_level, incentive_level)
#        print stay_choice
        stay_choices.extend(stay_choice)
        
    alt_leave_choices = []
    for incentive_level in range(0,3):
        incentive_key = 'dwell_time_inc_%s' %(str(incentive_level))
        incentive = determine_incentive_value(congestion_level, incentive_level)
        dwell_time = parsed_data[mode][congestion_level][user][incentive_key] + 15
        alt_leave_choice = create_choices_leave(parsed_data, user, mode, congestion_level, dwell_time, incentive)
        alt_leave_choices.extend(alt_leave_choice)
        
    choices = stay_choices + alt_leave_choices              
    return choices

def determine_choice_type(parsed_data, user, mode, congestion_level):
    chosen = parsed_data[mode][congestion_level][user]['dwell_status']
    if chosen == 'LLL':
        choices = choices_lll(parsed_data, user, mode, congestion_level)
    if chosen == 'SSS':
        choices =  choices_sss(parsed_data, user, mode, congestion_level)
    if chosen == 'LSS':
        choices =  choices_lss(parsed_data, user, mode, congestion_level)
    if chosen == 'LLS':
        choices = choices_lls(parsed_data, user, mode, congestion_level)
    return choices

def create_r_input_file(survey_data, modes = ['MRT', 'BUS']):
    rt_input = pd.DataFrame(columns = ['individual', 'gender', 'mode', 'decision', 'dwell_time', 'incentive', 'congestion', 'alt'])
    col_names = ['individual', 'gender', 'mode', 'decision', 'dwell_time', 'incentive', 'congestion', 'alt']
    parsed_data = sdpbm.get_parsed_data(survey_data)
    for mode in modes:
        for congestion_level in range(1,3):
#            print mode, congestion_level
            users = parsed_data[mode][congestion_level].keys()
            for user in users:
                if 'dwell_status' in parsed_data[mode][congestion_level][user]:
#                    print '\nmode: %s, congestion:  %s, user: %s' %(mode, str(congestion_level), str(user))
                    user_choice = determine_choice_type(parsed_data, user, mode, congestion_level)
                    choice_df = pd.DataFrame(user_choice, columns = col_names)
                    rt_input = rt_input.append(choice_df)
    nrow, _ = rt_input.shape
#    choice_id = np.repeat(range(nrow/2),2)
#    rt_input['choice_id'] = choice_id 
    rt_input['waiting_time'] = 0
    return rt_input
          

if __name__ == '__main__':
    survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)    
    modes = ['MRT', 'BUS']
    r_input_data = create_r_input_file(survey_data, modes)
    r_input_data.to_csv('r_input_data_bus_mrt.csv', index = False)
    modes = ['MRT']
    r_input_data = create_r_input_file(survey_data, modes)
    r_input_data.to_csv('r_input_data_mrt.csv', index = False)
    modes = ['BUS']
    r_input_data = create_r_input_file(survey_data, modes)
    r_input_data.to_csv('r_input_data_bus.csv', index = False)


    





















