import streamlit as st
import pandas as pd
import pickle
import numpy as np

# 1. Load the trained AI model (0.9074 Accuracy)
try:
    model = pickle.load(open('concrete_model.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: 'concrete_model.pkl' not found. Please ensure the model file is in the project folder.")

# 2. Page Configuration & Custom UI Styling
st.set_page_config(
    page_title="Concrete AI Pro | BCE Bhagalpur",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS for Adaptive Light/Dark Theme Look
st.markdown("""
    <style>
    /* Theme-aware variables */
    :root {
        --header-bg: #1e3a8a;
        --card-bg: rgba(255, 255, 255, 0.7);
        --text-color: #1e3a8a;
        --accent-gradient: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --header-bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-color: #60a5fa;
            --accent-gradient: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        }
    }

    /* Custom Header */
    .main-header {
        background-color: var(--header-bg);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    /* Card-like containers for inputs */
    div[data-testid="stVerticalBlock"] > div:has(div.stNumberInput) {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 45px;
        color: var(--text-color);
        font-weight: 800;
    }
    
    /* Buttons */
    .stButton>button {
        background: var(--accent-gradient);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - Profile & Project Info
with st.sidebar:
    st.image("https://img.icons8.com/external-beshi-flat-kerismaker/48/external-Concrete-Mix-construction-beshi-flat-kerismaker.png", width=100)
    st.title("Project Details")
    st.markdown("---")
    st.markdown("""
    **🎓 Student:** Vikash Kumar  
    **🏛️ Institution:** BCE Bhagalpur  
    **🔬 Algorithm:** Random Forest  
    **🎯 Accuracy:** 90.74%  
    """)
    st.success("Model Status: Online")
    st.write("---")
    st.caption("Final Year Major Project 2026")

# 4. Top Hero Section
st.markdown("""
    <div class="main-header">
        <h1>🏗️ Smart Concrete Mix Strength Predictor</h1>
        <p>Advanced Machine Learning for Civil Engineering Design Optimization</p>
    </div>
    """, unsafe_allow_html=True)

# 5. Input Section
st.subheader("📋 Mix Design Parameters")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 🧪 Binder Ingredients")
    cement = st.number_input("Cement (kg/m³)", value=300.0, step=10.0)
    water = st.number_input("Water (kg/m³)", value=150.0, step=5.0)
    slag = st.number_input("Blast Furnace Slag (kg/m³)", value=0.0, step=10.0)
    fly_ash = st.number_input("Fly Ash (kg/m³)", value=0.0, step=10.0)

with col2:
    st.markdown("### 🪨 Aggregates & Aging")
    sp = st.number_input("Superplasticizer (kg/m³)", value=0.0, step=0.5)
    coarse = st.number_input("Coarse Aggregate (kg/m³)", value=1000.0, step=50.0)
    fine = st.number_input("Fine Aggregate (kg/m³)", value=700.0, step=50.0)
    age = st.slider("Curing Age (Days)", 1, 365, 28)

# 6. Prediction Area
st.write("---")
if st.button("🚀 EXECUTE PREDICTION ANALYSIS", use_container_width=True):
    # Prepare Data
    input_dict = {
        'Cement': cement, 'Slag': slag, 'FlyAsh': fly_ash, 'Water': water,
        'SP': sp, 'CoarseAgg': coarse, 'FineAgg': fine, 'Age': age
    }
    input_df = pd.DataFrame([input_dict])
    
    # Prediction
    prediction = model.predict(input_df)[0]
    
    # Display Results in a Professional Layout
    res_col1, res_col2 = st.columns([1, 2])
    
    with res_col1:
        st.metric(label="Predicted Strength", value=f"{prediction:.2f} MPa")
    
    with res_col2:
        if prediction > 40:
            st.success("🌟 **High Strength Concrete (HSC)**")
            st.write("Ideal for pre-stressed structures, high-rise buildings, and heavy bridges.")
            st.balloons()
        elif prediction > 20:
            st.info("🏠 **Normal Strength Concrete (NSC)**")
            st.write("Suitable for general reinforced concrete structures and slabs.")
        else:
            st.warning("🧱 **Low Strength Concrete**")
            st.write("Recommended for non-structural masonry, filling, or plain concrete work.")

    # 7. Generate Downloadable Report
    report_content = f"""TECHNICAL PREDICTION REPORT
----------------------------------
Project: Concrete AI Pro
Institution: BCE Bhagalpur
Student: Vikash Kumar

MIX DESIGN:
- Cement: {cement} kg/m3
- Water: {water} kg/m3 (W/C Ratio: {water/cement:.2f})
- Slag: {slag} kg/m3
- Fly Ash: {fly_ash} kg/m3
- SP: {sp} kg/m3
- Aggregates: {coarse} (C) / {fine} (F)
- Age: {age} days

RESULT:
- Predicted Strength: {prediction:.2f} MPa
- Accuracy: 90.74%
----------------------------------"""

    st.download_button(
        label="📥 Download Technical Report",
        data=report_content,
        file_name=f"BCE_Mix_Report_{age}days.txt",
        mime="text/plain"
    )

# 8. Visual Analytics (Optional but Attractive)
if st.checkbox("Show Strength-Age Gain Estimation"):
    age_range = np.arange(1, 90)
    age_test = pd.DataFrame([input_dict] * len(age_range))
    age_test['Age'] = age_range
    strength_curve = model.predict(age_test)
    
    chart_data = pd.DataFrame({'Age (Days)': age_range, 'Strength (MPa)': strength_curve})
    st.line_chart(chart_data.set_index('Age (Days)'))
    st.caption("Estimated strength gain profile for this specific mix design.")
