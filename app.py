# app.py

import streamlit as st
import pandas as pd
import numpy as np
from src.modeling import load_model

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Restaurant Revenue Forecasting",
    page_icon="🍽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Custom CSS Styling (White plate, silver spoon theme)
# -------------------------------
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #e4e7eb);
}

/* Main title */
.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #2c3e50;
    text-align: center;
}

/* Plate container (white card) */
.plate {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}

/* Silver accent */
.silver {
    color: #C0C0C0;
    font-weight: bold;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    color: #27ae60;
    font-size: 32px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2c3e50, #4ca1af);
    color: white;
}

/* Button */
.stButton>button {
    background-color: #C0C0C0;
    color: black;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #a8a8a8;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Model and Data
# -------------------------------
@st.cache_resource
def get_model():
    return load_model("models/final_model.pkl")

@st.cache_data
def get_data():
    df = pd.read_csv("data/processed/daily_sales.csv")
    df = df.sort_values("Date")
    return df

model = get_model()
data = get_data()

# -------------------------------
# Header Section
# -------------------------------
st.markdown('<div class="main-title">🍽 Restaurant Revenue Forecasting</div>', unsafe_allow_html=True)

st.markdown("""
<div class="plate">
<span class="silver">AI-powered revenue prediction system</span><br>
Adjust inputs from sidebar and click Predict.
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.title("🥄 Input Controls")

day = st.sidebar.slider("📅 Day", 1, 31, 15)
month = st.sidebar.slider("📆 Month", 1, 12, 6)
weekday = st.sidebar.selectbox(
    "🗓 Weekday",
    options=[0,1,2,3,4,5,6],
    format_func=lambda x: ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][x]
)

quantity = st.sidebar.slider("🍽 Quantity Sold", 1, 5000, 200)

weekend = 1 if weekday >= 5 else 0

# -------------------------------
# Lag Features
# -------------------------------
lag_1 = data['Total_Revenue'].iloc[-1]
lag_2 = data['Total_Revenue'].iloc[-2]
lag_3 = data['Total_Revenue'].iloc[-3]

rolling_mean_3 = data['Total_Revenue'].iloc[-3:].mean()
rolling_mean_7 = data['Total_Revenue'].iloc[-7:].mean()

# -------------------------------
# Input DataFrame
# -------------------------------
input_data = pd.DataFrame({
    "Quantity": [quantity],
    "Day": [day],
    "Month": [month],
    "Weekday": [weekday],
    "Weekend": [weekend],
    "Lag_1": [lag_1],
    "Lag_2": [lag_2],
    "Lag_3": [lag_3],
    "Rolling_Mean_3": [rolling_mean_3],
    "Rolling_Mean_7": [rolling_mean_7]
})

# -------------------------------
# Layout columns
# -------------------------------
col1, col2 = st.columns([1,1])

# -------------------------------
# Prediction Section
# -------------------------------
with col1:
    st.markdown('<div class="plate">', unsafe_allow_html=True)

    if st.button("🔮 Predict Revenue"):

        prediction = model.predict(input_data)[0]

        st.metric(
            "💰 Predicted Revenue",
            f"${prediction:,.2f}",
            delta=f"{prediction - lag_1:,.2f} vs yesterday"
        )

        progress = min(int(prediction / data['Total_Revenue'].max() * 100), 100)
        st.progress(progress)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Comparison Chart
# -------------------------------
with col2:
    st.markdown('<div class="plate">', unsafe_allow_html=True)

    if 'prediction' in locals():

        compare_df = pd.DataFrame({
            "Revenue": [lag_3, lag_2, lag_1, prediction]
        }, index=["3 days ago", "2 days ago", "Yesterday", "Predicted"])

        st.subheader("📊 Revenue Comparison")
        st.bar_chart(compare_df)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Historical Chart
# -------------------------------
st.markdown('<div class="plate">', unsafe_allow_html=True)

st.subheader("📈 Historical Revenue Trend")
st.line_chart(data.set_index("Date")["Total_Revenue"])

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
<div style="text-align:center; color:gray;">
🥄 🍽 🍴 Machine Learning Portfolio Project<br>
Developed by Alisha
</div>
""", unsafe_allow_html=True)