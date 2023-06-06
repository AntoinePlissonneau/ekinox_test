#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 22:38:46 2023

@author: aplissonneau
"""
import os

# Ensure we are one the good directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from utils import ScoringModel, compute_manual_score




st.title('Prioritisation of student support')


st.markdown("""This dashboard aims to provide a decision tool for teachers which want
                to have insights about the improvement capacity of their students.
            Two interactives visualisations are implemented. The first one uses an improvability score
            estimated using machine learning. The second one uses an handcrafted improvability score
            which enable the user to parameter it by selecting the individual weights of three differents factors.""")
        
        
# =============================================================================
# Load data
# =============================================================================
st.header("Data to use")

st.markdown("Only if you want to import a custom dataset. The default dataset is already loaded.")
    
# Base dataset path
base_path = "data/student_data.csv"
data =  pd.read_csv(base_path)

# Enable the user to upload its own dataset
csv_file = st.file_uploader("Select your own csv file:", type=['csv'])

if st.button("Load the csv file"):
    if csv_file is None:
        csv_file = base_path
    data =  pd.read_csv(csv_file)

data["FullName"] = data.FirstName +" " + data.FamilyName


# =============================================================================
# School selection
# =============================================================================

st.header("School selection")
selected_school = st.multiselect('Select schools to include in the analysis:', data.school.unique())

all_options_school = st.checkbox("Select all schools (Uncheck if you want to select a subset of schools):", 
                          True)

if all_options_school:
    selected_school = data.school.unique()


# =============================================================================
# Students selection
# =============================================================================

st.header("Students selection")
selected_students = st.multiselect('Select students to include in the analysis:', 
                                   data.FullName[data.school.isin(selected_school)])

all_options_students = st.checkbox("Select all students (Uncheck if you want to select a subset of students):", 
                          True)

if all_options_students:
    selected_students = data.FullName


idx_mask = data.FullName.isin(selected_students) & data.school.isin(selected_school)
# TODO: Add school selection

# =============================================================================
# ML-based improvability score
# =============================================================================
st.header("ML-based improvability score")
#clean_df = pd.get_dummies(data)
model = joblib.load("models/booster.joblib")


# potential_grade = model.predict(clean_df[FEATURES])
improvability_score_ml = model.predict(data)

data["improvability_score_ml"] = improvability_score_ml
fig = px.scatter(data[idx_mask], x='FinalGrade', y="improvability_score_ml", 
                  hover_data=["FullName"])

st.plotly_chart(fig, use_container_width=True)

st.markdown("""You will find more information about each student by moving the mouse over 
            the data points.""")

# =============================================================================
# Manual improvability score
# =============================================================================

st.header("Manual improvability score")
st.markdown("""Select the coefficients based on your conception of which factor impact
        the most the improvability of a student.""")

# Select the parameters used to compute the improvability score
keys = ["studytime", "Dalc", "absences"]

col1, col2 = st.columns([2, 1])
col2.markdown("***")


# Create a slider for each parameter
coeff_dict = {}
for k in keys:
    coeff_dict.update({k: col2.slider(k, 0, 10, 5)})

# Compute the manual improvability score
score = compute_manual_score(data,  coeff_dict)

data["improvability_score_manual"] = score

st.markdown("""The graph above is updated on real time based on your selection. You 
            will find more information about each student by moving the mouse over 
            the data points.""")

fig = px.scatter(data[idx_mask], x="FinalGrade", y="improvability_score_manual",  
                 hover_data=["FullName"]+keys)

col1.plotly_chart(fig, use_container_width=True)





