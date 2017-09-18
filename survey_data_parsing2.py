# -*- coding: utf-8 -*-
"""
Created on Mon Sep 04 08:19:31 2017

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
for i, col in enumerate(survey_data.columns):
  print i, col

# data frame where the data would be stored
choice_data = pd.DataFrame(columns = ('user', 'gender', 'decision', 'incentive', 'congestion_level',
  'dwell_time_hr', 'dwell_time_min'))
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
              response20 = survey_data.Q20.iat[i]
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


for i, response20 in enumerate(survey_data.Q20):
  uid = survey_data['case.no'].iloc[i]
  gender = survey_data.Q52.iat[i]
  if response20 == 1:
      response22 = survey_data.Q22.iat[i]
      if response22 == 1:
          response24 = survey_data.Q24.iat[i]
          if response24 == 2:
              choice_data.loc[j] = [uid, gender, 1, 7, 1, survey_data.Q25_1_1.iat[i], survey_data.Q25_2_1.iat[i]]
              j = j+1
          if response24 == 1:
              choice_data.loc[j] = [uid, gender, 1, 0, 1, 0, 0]
              j = j+1 
      if response22 == 2:
          choice_data.loc[j] = [uid, gender, 1, 3, 1, survey_data.Q23_1_1.iat[i], survey_data.Q23_2_1.iat[i]]
          j = j+1
    
          choice_data.loc[j] = [uid, gender, 1, 7, 1, survey_data.Q23_1_2.iat[i], survey_data.Q23_2_2.iat[i]]
          j = j+1

  if response20 == 2:
      choice_data.loc[j] = [uid, gender, 1, 0, 1, survey_data.Q21_1_1.iat[i], survey_data.Q21_2_1.iat[i]]
      j = j + 1
    
      choice_data.loc[j] = [uid, gender, 1, 3, 1, survey_data.Q21_1_2.iat[i], survey_data.Q21_2_2.iat[i]]
      j = j+1
    
      choice_data.loc[j] = [uid, gender, 1, 7, 1, survey_data.Q21_1_3.iat[i], survey_data.Q21_2_3.iat[i]]
      j = j+1




choice_data['dwell_time'] = choice_data['dwell_time_hr']*60 + choice_data['dwell_time_min']

choice_data.to_csv('choice_data.csv', index = False)

choice_data

survey_data.Q20




###############################################################################
# people going home immediately
###############################################################################
case_no = [3,9,21,26,27,33,36,39,40,41,48,52,55,60,70,72,88,97,98,109,115,119,
           121,129,133,140,144,158,160,170,173,178]

leave_now_ind = survey_data['case.no'].isin(case_no)
leave_now_columns = ['Q14', 'Q16', 'Q18']

survey_data.loc[leave_now_ind,leave_now_columns]

###############################################################################
# people who want to wait
###############################################################################
# $0 incentive
case_no = [4,   7,  16,  17,  18,  32,  35,  42,  46,  53,  56,  64,  69,  71,  
           75,  76,  78,  80,  86,  87,  91, 102, 103, 141, 147, 152, 174, 177,
           185, 199]
stay_incentive_0_ind = survey_data['case.no'].isin(case_no)
incentive_0_columns = ['Q14', 'Q15_1_1', 'Q15_2_1', 'Q15_1_2', 'Q15_2_2', 'Q15_1_3', 'Q15_2_3' ]
survey_data.loc[stay_incentive_0_ind, incentive_0_columns]


# $5 incentive
case_no = [5,   8,  24,  29,  37,  61,  85, 111, 116, 118, 124, 125, 127, 156, 180, 188]
stay_incentive_5_ind = survey_data['case.no'].isin(case_no)
incentive_5_columns = ['Q14', 'Q16', 'Q17_1_1', 'Q17_1_2', 'Q17_2_1', 'Q17_2_2']
survey_data.loc[stay_incentive_5_ind, incentive_5_columns]


# $10 incentive
case_no = [25,  31,  34,  51,  54,  63,  95, 117, 122, 145, 167, 183, 198]
stay_incentive_10_ind = survey_data['case.no'].isin(case_no)
incentive_10_columns = ['Q14', 'Q16', 'Q18', 'Q19_1_1', 'Q19_2_1']
survey_data.loc[stay_incentive_10_ind, incentive_10_columns]

########################################################################################################################
# VERY CROWDED SITUATION
########################################################################################################################

# question 14: 14. Look at a figure below and answer the following questions.
# Suppose you want to take MRT to go home from Suntec City are and you are in very crowded situation after an event.
# Which option would you choose?
# A. Go home immediately. You will NOT get a seat and have to stand uncomfortably on the MRT (example picture 1) # 1
# B. Spend some time at Suntec City Mall and leave later when there are available seats on the MRT. (example picture 2) # 2

survey_data.shape
survey_data.columns[26]
survey_data.iloc[:, 26]

survey_data.Q14.isnull().sum()
survey_data.Q14.value_counts()

# follow up question when the user is ready to spend some time to avoid congestion
# 15. How much time are you willing to spend in Suntec City Mall to wait for the MRT to get less crowded?
#(1) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded? (please enter number of minutes)
survey_data.Q15_1_1
survey_data.Q15_2_1
#2 (2) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 5SGD coupon? (please enter number of minutes)
survey_data.Q15_1_2
survey_data.Q15_2_2
#(3) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 10SGD coupon? (please enter number of minutes)
survey_data.Q15_1_3
survey_data.Q15_2_3

# follow up question of 14 when the user is wants to leave immediately
#16. Look at a figure below and answer the following questions.
# Suppose you want to take MRT to go home from Suntec City area and you are in very crowded situation after an event.
#Which option would you choose?
# □ A. Go home immediately. You will NOT get a seat and have to stand uncomfortably on the MRT (example picture 1)
# □ B. Get 5 SGD worth of coupon and spend some time at Suntec City Mall and leave later when there are available seats on the MRT. (example picture 2)
survey_data.Q16

# 17. How much time are you willing to spend in Suntec City Mall to wait for the MRT to get less crowded?
# (1) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 5SGD coupon? (please enter number of minutes )

#(2) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 10SGD coupon? (please enter number of minutes )

#18. Look at a figure below and answer the following questions. Suppose you want to take MRT to go home from Suntec City area
# and you are in very crowded situation after an event.
#Which option would you choose?
#□ A. Go home immediately. You will NOT get a seat and have to stand uncomfortably on the MRT (example picture 1)
#□ B. Get 10 SGD worth of coupon and spend some time at Suntec City Mall and leave later when there are available seats on the MRT. (example picture 2)

# 19. How much time are you willing to spend in Suntec City Mall to wait for the MRT to get less crowded?
# (1) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 10SGD coupon? (please enter number of minutes )

####################################################################################################################
# LITTLE CROWDED SITUATION
####################################################################################################################

# 20. Look at a figure below and answer the following questions. Suppose you want to take MRT to go home from Suntec City area
# and you are in little crowded situation after an event.
#Which option would you choose?
#□ A. Go home immediately. You will NOT get a seat but you can stand comfortably on the MRT (example picture 1)
#□ B. Spend some time at Suntec City Mall and leave later when there are available seats on the MRT. (example picture 2)

# 21. How much time are you willing to spend in Suntec City Mall to wait for the MRT to get less crowded?
#
# (1) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded? (please enter number of minutes )
# (2) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 3SGD coupon? (please enter number of minutes)
# (3) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 7SGD coupon? (please enter number of minutes )

# 22. Look at a figure below and answer the following questions. Suppose you want to take MRT to go home from
# Suntec City area and you are in little crowded situation after an event.
#Which option would you choose?
#□ A. Go home immediately. You will NOT get a seat but you can stand comfortably on the MRT (example picture 1)
#□ B. Get 3 SGD worth of coupon and spend some time at Suntec City Mall and leave later when there are available seats on the MRT. (example picture 2)

#23. How much time are you willing to spend in Suntec City Mall to wait for the MRT to get less crowded?
# (1) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 3SGD coupon? (please enter number of minutes )

#(2) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 7SGD coupon? (please enter number of minutes )

#24. Look at a figure below and answer the following questions. Suppose you want to take MRT to go home from Suntec City area and you are in little crowded situation after an event.
# Which option would you choose?
# □ A. Go home immediately. You will NOT get a seat but you can stand comfortably on the MRT (example picture 1)
# □ B. Get 7 SGD worth of coupon and spend some time at Suntec City Mall and leave later when there are available seats on the MRT. (example picture 2)

# 25. How much time are you willing to spend in Suntec City Mall to wait for the MRT to get less crowded?
# (1) How much time are you willing to spend in Suntec to wait for the MRT to get less crowded with 7SGD coupon? (please enter number of minutes )

# Difference are
# 1. coupon value
# 2. congestion status

###############################################################################
# Code for highe congestion level
###############################################################################
# Q52 gender

###############################################################################
# checking if it is working fine
###############################################################################
# randomly pick one user from the choice_data
n, _ = choice_data.shape
i = np.random.choice(range(n))
user = choice_data.user.iat[i]

user = 3
ind = choice_data.user == user
choice_data.loc[ind]

print 'user: ', user
for i in range(np.sum(ind)):
# print 'Incentive: ', choice_data.loc[ind].incentive.iloc[i]
# print 'Wait Time (in Hrs): ', choice_data.loc[ind].dwell_time_hr.iloc[i]
# print 'Wait Time (in Mins): ', choice_data.loc[ind].dwell_time_min.iloc[i]
# print '\n'

  print "Incentive Wait Time(in Hrs) Wait Time (in Mins)"
  print choice_data.loc[ind].incentive.iloc[i], choice_data.loc[ind].dwell_time_hr.iloc[i], choice_data.loc[ind].dwell_time_min.iloc[i]

ind = survey_data['case.no'] == user
ss = survey_data.loc[ind]
if ss.Q14.values[0] == 2:
  print ss.Q15_1_1.values[0], ss.Q15_2_1.values[0]
  print ss.Q15_1_2.values[0], ss.Q15_2_2.values[0]
  print ss.Q15_1_3.values[0], ss.Q15_2_3.values[0]
elif ss.Q14.values[0] == 1:
  if ss.Q16.values[0] == 2:
      print ss.Q17_1_1.values[0], ss.Q17_2_1.values[0]
      print ss.Q17_1_2.values[0], ss.Q17_2_2.values[0]
  elif ss.Q16.values[0] == 1:
      if ss.Q16.values[0] == 2:
          print ss.Q19_1_1.values[0], ss.Q19_2_1.values[0]

useful_col = ['case.no', 'Q14', 'Q15_1_1', 'Q15_1_2', 'Q15_1_3','Q16', 'Q17_1_1', 'Q17_1_2', 'Q18', 'Q19_1_1', 'Q19_2_1' ]
survey_data.loc[ind, useful_col]
