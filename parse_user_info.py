# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:15:31 2017

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

for col in survey_data.columns:
    print col
    
survey_data.Q52
survey_data.Q53
survey_data.Q54

n_row, _ = survey_data.shape

user_info = {}
for i in range(200):
    id = int(survey_data['case.no'].iloc[i])
    user_info[id] = {}
    if survey_data.Q52.iloc[i] == 1:
        user_info[id]['gender'] = 1
    if survey_data.Q52.iloc[i] == 2:
        user_info[id]['gender'] = 2
