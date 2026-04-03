import streamlit as st
import pandas as pd
import pickle
import numpy as np
from scipy.interpolate import UnivariateSpline
import os

# Define multiple possible paths for the model file
POSSIBLE_PATHS = [
    'concrete_strength_model.pkl',
    '/content/drive/Othercomputers/VIKASH HP/Documents/GitHub/Concrete-Strength-AI/concrete_strength_model.pkl'
]

# 1. Load the trained AI model and scaler using path redundancy
model_components = None
for path in POSSIBLE_PATHS:
    if os.path.exists(path):
        try:
            with open(path, 'rb') as file:
                model_components = pickle.load(file)
            break
        except Exception as e:
            continue

if model_components is None:
    st.error("Error: Could not find 'concrete_strength_model.pkl' in local directory or Drive path.")
    st.stop()

model = model_components['model']
scaler = model_components['scaler']

# 2. Page Configuration
st.set_page_config(page_title="Concrete AI Pro", page_icon="🏗️")

# Sidebar & Info
st.sidebar.title("Project Personnel")
st.sidebar.info("Lead: Vikash Kumar (D23177)")

# Main Header
st.title("🏗️ Smart Concrete Mix Strength Predictor")

# Input Section
st.subheader("📋 Mix Design Parameters")
col1, col2 = st.columns(2)
with col1:
    cement = st.number_input("Cement (kg/m³)", value=300.0)
    water = st.number_input("Water (kg/m³)", value=150.0)
    slag = st.number_input("Slag (kg/m³)", value=0.0)
    fly_ash = st.number_input("Fly Ash (kg/m³)", value=0.0)
with col2:
    sp = st.number_input("Superplasticizer (kg/m³)", value=0.0)
    coarse = st.number_input("Coarse Aggregate (kg/m³)", value=1000.0)
    fine = st.number_input("Fine Aggregate (kg/m³)", value=700.0)
    age = st.slider("Curing Age (Days)", 1, 365, 28)

wc_ratio = water / cement if cement != 0 else 0
input_dict = {'Cement': cement, 'Slag': slag, 'FlyAsh': fly_ash, 'Water': water, 'SP': sp, 'CoarseAgg': coarse, 'FineAgg': fine, 'Age': age, 'WC_Ratio': wc_ratio}
feature_columns = ['Cement', 'Slag', 'FlyAsh', 'Water', 'SP', 'CoarseAgg', 'FineAgg', 'Age', 'WC_Ratio']
input_df = pd.DataFrame([input_dict], columns=feature_columns)

if st.button("🚀 EXECUTE PREDICTION"):
    scaled_input = scaler.transform(input_df)
    prediction = model.predict(scaled_input)[0]
    st.metric(label="Predicted Strength", value=f"{prediction:.2f} MPa")

# Visual Analytics with Smoothing
if st.checkbox("Show Smooth Strength-Age Gain Curve"):
    age_range = np.arange(1, 101)
    plot_data = []
    for day in age_range:
        row = input_dict.copy()
        row['Age'] = day
        plot_data.append(row)

    age_df = pd.DataFrame(plot_data, columns=feature_columns)
    raw_strength = model.predict(scaler.transform(age_df))

    spline = UnivariateSpline(age_range, raw_strength, s=50)
    smooth_strength = spline(age_range)

    chart_df = pd.DataFrame({'Age (Days)': age_range, 'Raw Prediction': raw_strength, 'Smoothed Growth': smooth_strength})
    st.line_chart(chart_df.set_index('Age (Days)'))
    st.caption("The smoothed curve represents a more realistic continuous hydration process.")
