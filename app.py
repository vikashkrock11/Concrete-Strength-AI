import streamlit as st
import pandas as pd
import pickle
import numpy as np
from scipy.interpolate import make_interp_spline
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

st.set_page_config(page_title="Concrete AI Pro", page_icon="🏗️")

st.sidebar.title("Project Personnel")
st.sidebar.info("Lead: Vikash Kumar (D23177)")

st.title("🏗️ Smart Concrete Mix Strength Predictor")

st.subheader("📋 Mix Design Parameters")
col1, col2 = st.columns(2)
with col1:
    cement = st.number_input("Cement (kg/m³)", value=300.0, min_value=0.01) # Ensure positive non-zero
    water = st.number_input("Water (kg/m³)", value=150.0, min_value=0.01)   # Ensure positive non-zero
    slag = st.number_input("Slag (kg/m³)", value=0.0, min_value=0.0)     # Allow zero, but not negative
    fly_ash = st.number_input("Fly Ash (kg/m³)", value=0.0, min_value=0.0) # Allow zero, but not negative
with col2:
    sp = st.number_input("Superplasticizer (kg/m³)", value=0.0, min_value=0.0) # Allow zero, but not negative
    coarse = st.number_input("Coarse Aggregate (kg/m³)", value=1000.0, min_value=0.01) # Ensure positive non-zero
    fine = st.number_input("Fine Aggregate (kg/m³)", value=700.0, min_value=0.01)   # Ensure positive non-zero
    age = st.slider("Curing Age (Days)", min_value=1, max_value=365, value=28)

# Adding a check for cement before calculating wc_ratio
if cement == 0:
    st.warning("Cement cannot be zero for a valid concrete mix. Setting to a minimal value for calculation.")
    wc_ratio = water / 0.01 # Use a minimal value for calculation if user somehow bypasses min_value
else:
    wc_ratio = water / cement

input_dict = {'Cement': cement, 'Slag': slag, 'FlyAsh': fly_ash, 'Water': water, 'SP': sp, 'CoarseAgg': coarse, 'FineAgg': fine, 'Age': age, 'WC_Ratio': wc_ratio}
feature_columns = ['Cement', 'Slag', 'FlyAsh', 'Water', 'SP', 'CoarseAgg', 'FineAgg', 'Age', 'WC_Ratio']
input_df = pd.DataFrame([input_dict], columns=feature_columns)

if st.button("🚀 EXECUTE PREDICTION"):
    scaled_input = scaler.transform(input_df)
    prediction = model.predict(scaled_input)[0]

    # Display physically plausible prediction, considering zero cement
    if cement < 0.01: # Check against the min_value used
        st.metric(label="Predicted Strength", value=f"0.00 MPa (Cement too low)")
        st.error("A concrete mix requires a positive amount of cement to gain strength.")
    else:
        st.metric(label="Predicted Strength", value=f"{prediction:.2f} MPa")

if st.checkbox("Show Smooth Strength-Age Gain Curve"):
    # Generate a range of ages for prediction
    age_range = np.linspace(1, 100, 100)
    plot_data = []
    for day in age_range:
        row = input_dict.copy()
        row['Age'] = day
        plot_data.append(row)

    age_df = pd.DataFrame(plot_data, columns=feature_columns)

    # Handle case where cement is too low for a realistic curve
    if cement < 0.01:
        raw_strength = np.zeros(len(age_range)) # Predict 0 strength if cement is practically zero
        st.warning("Strength growth curve cannot be generated meaningfully for mixes with virtually no cement.")
    else:
        raw_strength = model.predict(scaler.transform(age_df))

    # Use a higher-order Polynomial fit for better smoothing of tree-based steps
    z = np.polyfit(age_range, raw_strength, 3)
    p = np.poly1d(z)
    smooth_strength = p(age_range)

    chart_df = pd.DataFrame({
        'Age (Days)': age_range,
        'Raw Prediction': raw_strength,
        'Smoothed Growth Curve': smooth_strength
    })

    st.line_chart(chart_df.set_index('Age (Days)'))
    st.caption("The red line (Smoothed Growth) represents the continuous chemical gain in strength over time.")
