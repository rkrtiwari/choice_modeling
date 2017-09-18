# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 11:19:38 2017

@author: tiwarir
"""

import os
import pandas as pd

def parse_user_response(survey_data):
    choice_data = pd.DataFrame(columns = ('user', 'gender', 'decision', 'incentive', 'congestion_level', 'dwell_time_hr', 'dwell_time_min'))
    j = 0
    
    for i, response14 in enumerate(survey_data.Q14):
        uid = survey_data['case.no'].iloc[i]
        gender = survey_data.Q52.iat[i]
        
        if response14 == 1:
              response16 = survey_data.Q16.iat[i]
              if response16 == 1:
                  response18 = survey_data.Q18.iat[i]
                  if response18 == 2:
                      choice_data.loc[j] = [uid, gender, 1, 10, 2, survey_data.Q19_1_1.iat[i], survey_data.Q19_2_1.iat[i]]
                      j = j+1
                  if response18 == 1:
                      choice_data.loc[j] = [uid, gender, 1, 0, 2, 0, 0]
                      j = j+1
              if response16 == 2:
                  choice_data.loc[j] = [uid, gender, 1, 5, 2, survey_data.Q17_1_1.iat[i], survey_data.Q17_2_1.iat[i]]
                  j = j+1
                  choice_data.loc[j] = [uid, gender, 1, 10, 2, survey_data.Q17_1_2.iat[i], survey_data.Q17_2_2.iat[i]]
                  j = j+1
        if response14 == 2:
              choice_data.loc[j] = [uid, gender, 1, 0, 2, survey_data.Q15_1_1.iat[i], survey_data.Q15_2_1.iat[i]]
              j = j + 1
              choice_data.loc[j] = [uid, gender, 1, 5, 2, survey_data.Q15_1_2.iat[i], survey_data.Q15_2_2.iat[i]]
              j = j+1
              choice_data.loc[j] = [uid, gender, 1, 10, 2, survey_data.Q15_1_3.iat[i], survey_data.Q15_2_3.iat[i]]
              j = j+1
              
    choice_data['dwell_time'] = choice_data['dwell_time_hr']*60 + choice_data['dwell_time_min']
              
    return choice_data

if __name__ == '__main__':
    os.chdir("C:\\Users\\tiwarir\\Documents\\behavior_learning\\python_code")
    survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)
    choice_data_old = parse_user_response(survey_data)
    


