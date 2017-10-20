# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 09:02:45 2017

@author: tiwarir
"""
import numpy as np
import pandas as pd
import prepare_input_file_for_mlogit_taxi as pifmt
import prepare_input_file_for_mlogit_bus_mrt as pifmbm
reload(pifmt)
reload(pifmbm)

def create_input_file():
    survey_data = pd.read_excel('Behavior change for weekend SCC (Dec.5-6).xlsx', sheetname = 'SCC 5-6 Dec', skiprows = 0)
    df_bus_mrt =  pifmbm.create_r_input_file(survey_data)
    df_taxi = pifmt.create_r_input_file(survey_data)
    df = pd.concat([df_bus_mrt, df_taxi])
    nrow, _ = df.shape
    choice_id = np.repeat(range(nrow/2),2)
    df['choice_id'] = choice_id
    df.to_csv('r_input_data.csv', index = False)
    return df
    
    
if __name__ == '__main__':
    df = create_input_file()

    