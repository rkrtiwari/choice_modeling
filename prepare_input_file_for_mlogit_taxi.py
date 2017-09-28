# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 10:43:48 2017

@author: tiwarir
"""
import os
import pandas as pd

mode = 'taxi' 
congestion_level = 2
input_filename = "choice_data_%s_cong_%s.csv" %(mode,congestion_level)
choice_data = pd.read_csv(input_filename)

def create_choice_df(input_filename):
    user_choice = pd.DataFrame(columns = ('user', 'gender', 'DT', 'WT', 'incentive', 'decision', 'mode'))
    j = 0
    users = choice_data.user.values
    
    for user in users:
        ind = choice_data.user == user
        user_df = choice_data.loc[ind,]
        user = user_df.user.values[0]
        gender = user_df.gender.values[0]
        DT = user_df.dwell_time.values[0]
        WT = user_df.waiting_time_in_q.values[0]
        incentive = user_df.incentive.values[0]
        congestion_level = user_df.congestion_level.values[0]
        if DT > 0:
            accepted = [user, gender, DT, 0, incentive, 1, 'stay']
            if congestion_level == 1:
                rejected = [user, gender, 0, 15, 0, 0, 'leave']
            if congestion_level == 2:
                rejected = [user, gender, 0, 30, 0, 0, 'leave']
        if WT > 0:
            if congestion_level == 1:
                accepted = [user, gender, 0, 15, 0, 1, 'leave']
            if congestion_level == 2:
                accepted = [user, gender, 0, 30, 0, 1, 'leave']
            rejected = [user, gender, 60, 0, incentive, 0, 'stay']
            
        user_choice.loc[j] = accepted
        j = j+1
        user_choice.loc[j] = rejected
        j = j+1
        
    return user_choice
        
            
if __name__ == '__main__':
    os.chdir("C:\\Users\\tiwarir\\Documents\\behavior_learning\\final_code")
    mode = 'taxi'   #options 'BUS', 'MRT'
    for congestion_level in [1,2]:
        input_filename = "choice_data_%s_cong_%s.csv" %(mode,congestion_level)
        choice_data = pd.read_csv(input_filename)
        output_filename = 'r_input_data_' + mode.lower() + '_congestion_level_' + str(congestion_level) + '.csv'
        df = create_choice_df(choice_data)
        df.to_csv(output_filename, index = False)

        
            
            
            
            
            