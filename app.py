import streamlit as st
import pandas as pd
import pickle
import numpy as np

# 1. Load the trained AI model
# Ensure 'concrete_model.pkl' is in the same folder as this app.py
model = pickle.load(open('concrete_model.pkl', 'rb'))

# 2. Set up the Website Title
st.set_page_config(page_title="Concrete Strength Predictor")
st.title("🏗️ Concrete Strength AI Predictor")
st.write("Enter the mix ingredients below to predict the Compressive Strength (MPa).")

# 3. Create Input Sliders/Boxes for the 8 Ingredients
st.header("Mix Design Inputs")

col1, col2 = st.columns(2)

with col1:
    cement = st.number_input("Cement (kg/m³)", value=300.0)
    slag = st.number_input("Blast Furnace Slag (kg/m³)", value=0.0)
    fly_ash = st.number_input("Fly Ash (kg/m³)", value=0.0)
    water = st.number_input("Water (kg/m³)", value=150.0)

with col2:
    sp = st.number_input("Superplasticizer (kg/m³)", value=0.0)
    coarse = st.number_input("Coarse Aggregate (kg/m³)", value=1000.0)
    fine = st.number_input("Fine Aggregate (kg/m³)", value=700.0)
    age = st.slider("Curing Age (Days)", 1, 365, 28)

# 4. The Prediction Button (Updated with DataFrame logic)
if st.button("Predict Compressive Strength"):
    # Create a dictionary matching your training column names exactly
    input_dict = {
        'Cement': cement,
        'Slag': slag,
        'FlyAsh': fly_ash,
        'Water': water,
        'SP': sp,
        'CoarseAgg': coarse,
        'FineAgg': fine,
        'Age': age
    }
    
    # Convert to DataFrame
    input_df = pd.DataFrame([input_dict])
    
    # Make the prediction
    prediction = model.predict(input_df)[0]
    
    # Show the result
    st.success(f"### Predicted Strength: {prediction:.2f} MPa")
    
    # Engineering Interpretation
    if prediction > 40:
        st.balloons()
        st.info("Grade Category: High Strength Concrete")
    elif prediction > 20:
        st.info("Grade Category: Normal Strength Concrete")
    else:
        st.warning("Grade Category: Low Strength Concrete")

        # --- ADD THIS FOR THE DOWNLOAD BUTTON ---
    # 5. Prepare the report text
    report_text = f"""
    Concrete Strength Prediction Report
    -----------------------------------
    Mix Design Inputs:
    - Cement: {cement} kg/m³
    - Blast Furnace Slag: {slag} kg/m³
    - Fly Ash: {fly_ash} kg/m³
    - Water: {water} kg/m³
    - Superplasticizer: {sp} kg/m³
    - Coarse Aggregate: {coarse} kg/m³
    - Fine Aggregate: {fine} kg/m³
    - Curing Age: {age} days
    
    Prediction Result:
    - Compressive Strength: {prediction:.2f} MPa
    """

    # 6. Create the Download Button
    st.download_button(
        label="Download Prediction Report",
        data=report_text,
        file_name=f"Concrete_Strength_Report_{age}days.txt",
        mime="text/plain"
    )