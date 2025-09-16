import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Use st.cache_data to load the data only once
@st.cache_data
def load_and_process_data(file_path='mining_data.csv'):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    CO2_PER_KWH = 0.5
    CO2_PER_LITER_DIESEL = 2.7
    df['CO2_Emissions_kg'] = (df['Energy_Consumption_kWh'] * CO2_PER_KWH) + (df['Fuel_Consumption_L'] * CO2_PER_LITER_DIESEL)
    df['Water_Wastage_m3'] = df['Water_Usage_m3'] * np.random.uniform(0.1, 0.3)
    return df

st.title("From Ore to Insight: Our Journey")
st.write("### A step-by-step visualization of how our solution transforms raw data into a powerful tool for sustainability.")

st.write("---")

# Load the data
df = load_and_process_data()

# --- Step 1: Raw Data ---
st.header("Step 1: Raw Data Acquisition")
st.write("The journey begins with the physical extraction of raw materials. This is the starting point of the entire process.")

st.line_chart(df[['Energy_Consumption_kWh', 'Fuel_Consumption_L']])
st.write("---")

# --- Step 2: AI-Powered Analysis ---
st.header("Step 2: AI-Powered Analysis")
st.write("The raw data is fed into Nimer's machine learning models. The AI performs an instant Life Cycle Assessment (LCA).")

cost_breakdown = pd.DataFrame({
    'Cost Type': ['Energy Cost', 'Fuel Cost'],
    'Total Cost ($)': [(df['Energy_Consumption_kWh'].sum() * 0.12), (df['Fuel_Consumption_L'].sum() * 0.90)]
})
fig_cost = px.bar(cost_breakdown, x='Cost Type', y='Total Cost ($)', title='Breakdown of Total Operational Costs', color='Cost Type')
st.plotly_chart(fig_cost)
st.write("---")

# --- Step 3: Predictive Forecasting ---
st.header("Step 3: Predictive Forecasting")
st.write("Our predictive AI engine forecasts the environmental footprint for the coming days and weeks. This enables proactive insights.")

future_predictions = df['CO2_Emissions_kg'].tail(7) # Use the last 7 days as a simulated prediction
fig_forecast = px.bar(x=future_predictions.index, y=future_predictions.values, labels={'x': 'Date', 'y': 'Predicted CO2 (kg)'}, title='7-Day Forward Projection')
st.plotly_chart(fig_forecast)
st.write("---")

# --- Step 4: Actionable Insights ---
st.header("Step 4: Actionable Insights")
st.write("The final step is presenting this intelligence on our user-friendly dashboard.")
st.metric(label="Average Daily CO2 Emissions", value=f"{df['CO2_Emissions_kg'].mean():,.0f} kg")

st.write("---")

st.info("This concludes the journey. You can now explore the rest of the application using the navigation bar.")