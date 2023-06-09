#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 22:25:17 2023

@author: aplissonneau
"""

import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from utils import ScoringModel
    

    
FEATURES = ['Dalc',
             'Medu',
             'absences',
             'age',
             'failures',
             'goout',
             'studytime',
             'schoolsup_yes',
             'higher_yes',
             'internet_yes',
             'Mjob_health',
             'Mjob_other',
             'Fjob_teacher']

TARGET = "FinalGrade"

data =  pd.read_csv("data/student_data.csv")

n_estimators = 9000
gb_reg = GradientBoostingRegressor(max_depth=3, n_estimators=n_estimators, learning_rate=0.0003, 
                                  subsample=0.5)

model = ScoringModel(FEATURES, TARGET, gb_reg)

print("Start training... ")
model.fit(data)

print("Saving to models folder ...")

joblib.dump(model, 'models/booster.joblib') 

print("DONE")

    

    