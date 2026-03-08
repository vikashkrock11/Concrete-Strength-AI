import streamlit as st
import pandas as pd
import pickle
import numpy as np
from fpdf import FPDF
import base64

# 1. Load the trained AI model
try:
    # Handle both direct model pickling and dictionary-style pickling
    model_data = pickle.load(open('concrete_model.pkl', 'rb'))
    if isinstance(model_data, dict):
        model = model_data['model']
    else:
        model = model_data
except FileNotFoundError:
    st.error("Error: 'concrete_model.pkl' not found. Please ensure the model file is in the project folder.")

# 2. Page Configuration & Custom UI Styling
st.set_page_config(
    page_title="Concrete AI Pro | BCE Bhagalpur",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Adaptive Light/Dark Theme Look
st.markdown("""
    <style>
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

    header[data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stAppDeployButton { display: none !important; }
    #MainMenu { display: none !important; }
    footer { visibility: hidden; }

    .main-header {
        background-color: var(--header-bg);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    .team-line { font-size: 0.9rem; opacity: 0.9; margin-top: 10px; font-style: italic; }
    
    div[data-testid="stVerticalBlock"] > div:has(div.stNumberInput) {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stMetricValue"] { font-size: 45px; color: var(--text-color); font-weight: 800; }
    
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

# 3. PDF Generation Tool
def generate_pdf(inputs, prediction, student_info, team_list):
    pdf = FPDF()
    pdf.add_page()
    
    # Header Banner
    pdf.set_fill_color(30, 58, 138) 
    pdf.rect(0, 0, 210, 40, 'F')
    
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, "Concrete Strength Analysis Report", ln=True, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "BCE Bhagalpur - Civil Engineering - Group 5", ln=True, align='C')
    
    pdf.ln(20)
    pdf.set_text_color(0, 0, 0)
    
    # Project Info
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Project Personnel Information", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, f"Designed By: {student_info['name']} (Roll: {student_info['roll']})", ln=True)
    pdf.multi_cell(0, 7, f"Team Members: {team_list}")
    
    pdf.ln(10)
    
    # Mix Design Table
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Mix Design Parameters", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(100, 10, "Ingredient Component", 1, 0, 'L', True)
    pdf.cell(90, 10, "Quantity (kg/m3)", 1, 1, 'C', True)
    
    pdf.set_font("Arial", '', 12)
    for key, value in inputs.items():
        pdf.cell(100, 10, str(key), 1)
        pdf.cell(90, 10, f"{value:.2f}", 1, 1, 'C')
    
    pdf.ln(10)
    
    # Result Box
    pdf.set_draw_color(30, 58, 138)
    pdf.set_line_width(1)
    pdf.set_fill_color(230, 242, 255)
    pdf.rect(10, pdf.get_y(), 190, 30, 'DF')
    
    pdf.set_y(pdf.get_y() + 5)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Predicted Compressive Strength: {prediction:.2f} MPa", ln=True, align='C')
    pdf.set_font("Arial", 'I', 11)
    pdf.cell(0, 10, "Model Accuracy: 94.66% | Analysis completed successfully.", ln=True, align='C')
    
    return bytes(pdf.output())

# 4. Data & Sidebar
student_info = {
    "name": "Vikash Kumar",
    "roll": "D23177",
    "reg": "23101108906",
    "inst": "BCE Bhagalpur"
}
team_names = "Vikash, Ritika, Sarfe, Harish, Rishikesh, Sahil, Astitva"

with st.sidebar:
    st.image("https://img.icons8.com/external-beshi-flat-kerismaker/48/external-Concrete-Mix-construction-beshi-flat-kerismaker.png", width=100)
    st.title("Group 5 Project")
    st.markdown("---")
    st.markdown(f"""
    **👤 Lead:** **{student_info['name']}** **🆔 Roll No:** {student_info['roll']}  
    **📝 Reg No:** {student_info['reg']}  
    **🏛️ Dept:** Civil Engineering  
    **🎯 Accuracy:** 94.66%
    """)
    st.divider()
    with st.expander("👥 Team Members", expanded=True):
        st.write(team_names)
    st.success("Model Status: Online")

# 5. Main Content
st.markdown(f"""
    <div class="main-header">
        <h1>🏗️ Smart Concrete Mix Strength Predictor</h1>
        <p style="font-size: 1.2rem;">Advanced Machine Learning for Civil Engineering Design Optimization</p>
        <div class="team-line"><b>Developed By Group 5:</b> {team_names}</div>
    </div>
    """, unsafe_allow_html=True)

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

# Input storage
input_dict = {
    'Cement': cement, 'Slag': slag, 'FlyAsh': fly_ash, 'Water': water,
    'SP': sp, 'CoarseAgg': coarse, 'FineAgg': fine, 'Age': age
}

# 6. Prediction Logic
st.write("---")
if st.button("🚀 EXECUTE PREDICTION ANALYSIS", use_container_width=True):
    # Convert to DataFrame
    df = pd.DataFrame([input_dict])
    
    # --- Feature Engineering to reach 11 features ---
    df['Water_Cement_Ratio'] = water / (cement + 0.001)
    df['Total_Binder'] = cement + slag + fly_ash
    df['Water_Binder_Ratio'] = water / (df['Total_Binder'] + 0.001)
    
    try:
        prediction = model.predict(df)[0]
        
        res_col1, res_col2 = st.columns([1, 2])
        with res_col1:
            st.metric(label="Predicted Strength", value=f"{prediction:.2f} MPa")
        
        with res_col2:
            if prediction > 40: st.success("🌟 **High Strength Concrete (HSC)**")
            elif prediction > 20: st.info("🏠 **Normal Strength Concrete (NSC)**")
            else: st.warning("🧱 **Low Strength Concrete**")

        # PDF Button
        pdf_bytes = generate_pdf(input_dict, prediction, student_info, team_names)
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"BCE_Mix_Report_{age}days.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Prediction failed: {e}")

# 7. Visual Analytics
if st.checkbox("Show Strength-Age Gain Estimation"):
    age_range = np.arange(1, 91)
    plot_data_rows = []
    for day in age_range:
        current_row = input_dict.copy()
        current_row['Age'] = day
        plot_data_rows.append(current_row)
        
    age_test_df = pd.DataFrame(plot_data_rows)
    # Apply engineering to the curve as well
    age_test_df['Water_Cement_Ratio'] = water / (cement + 0.001)
    age_test_df['Total_Binder'] = cement + slag + fly_ash
    age_test_df['Water_Binder_Ratio'] = water / (age_test_df['Total_Binder'] + 0.001)
    
    strength_curve = model.predict(age_test_df)
    chart_data = pd.DataFrame({'Age (Days)': age_range, 'Strength (MPa)': strength_curve})
    st.line_chart(chart_data.set_index('Age (Days)'))
