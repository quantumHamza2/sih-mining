import streamlit as st
import time

st.title("From Ore to Insight: Our Journey")
st.write("### A step-by-step visualization of how our solution transforms raw data into a powerful tool for sustainability.")

st.write("---")

# Use st.session_state to manage the progress
if 'progress_value' not in st.session_state:
    st.session_state.progress_value = 0

# Create the progress bar
st.markdown("#### Project Progress")
progress_bar = st.progress(st.session_state.progress_value)

# Define the journey steps and their progress values
journey_steps = {
    "Start": 0,
    "Raw Data": 25,
    "AI Analysis": 50,
    "Predictive AI": 75,
    "Dashboard": 100
}

# Create buttons to update the progress
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("Start", use_container_width=True):
        st.session_state.progress_value = journey_steps["Raw Data"]
with col2:
    if st.button("Step 1: Data", use_container_width=True):
        st.session_state.progress_value = journey_steps["Raw Data"]
with col3:
    if st.button("Step 2: Analysis", use_container_width=True):
        st.session_state.progress_value = journey_steps["AI Analysis"]
with col4:
    if st.button("Step 3: Predictions", use_container_width=True):
        st.session_state.progress_value = journey_steps["Predictive AI"]
with col5:
    if st.button("Step 4: Insights", use_container_width=True):
        st.session_state.progress_value = journey_steps["Dashboard"]

# Animate the progress bar to the new value
for i in range(st.session_state.progress_value + 1):
    progress_bar.progress(i)
    time.sleep(0.001)

st.write("---")

# Display the content for each step based on the progress value
if st.session_state.progress_value == journey_steps["Start"]:
    st.markdown("###  Click a button above to begin the journey!")

if st.session_state.progress_value >= journey_steps["Raw Data"]:
    st.header("Step 1: Raw Data Acquisition ")
    st.write("The journey begins at the mine site. Using sensors, we acquire a continuous stream of real-time operational data.")
    st.write("---")
    
if st.session_state.progress_value >= journey_steps["AI Analysis"]:
    st.header("Step 2: AI-Powered Analysis ")
    st.write("The collected data is fed into Nimer's machine learning models. The AI performs an instant Life Cycle Assessment (LCA).")
    st.write("---")
    
if st.session_state.progress_value >= journey_steps["Predictive AI"]:
    st.header("Step 3: Predictive Forecasting ")
    st.write("Our predictive AI engine forecasts the environmental footprint for the coming days and weeks. This enables proactive insights.")
    st.write("---")
    
if st.session_state.progress_value >= journey_steps["Dashboard"]:
    st.header("Step 4: Actionable Insights ")
    st.write("The final step is presenting this intelligence on our user-friendly dashboard.")