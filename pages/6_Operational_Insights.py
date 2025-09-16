import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Use st.cache_data to load the data only once
@st.cache_data
def load_and_process_data(file_path='mining_data.csv'):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    CO2_PER_KWH = 0.5
    CO2_PER_LITER_DIESEL = 2.7
    df['CO2_Emissions_kg'] = (df['Energy_Consumption_kWh'] * CO2_PER_KWH) + (df['Fuel_Consumption_L'] * CO2_PER_LITER_DIESEL)
    return df

# --- Page Content ---
st.title(" Operational & Business Insights")
st.write("### Deriving key metrics to optimize efficiency and reduce costs.")

df = load_and_process_data()

st.write("---")

# --- Efficiency Metrics ---
st.header("1. Operational Efficiency Metrics")
st.write("These metrics show the environmental and energy impact per unit of ore processed.")

# Calculate Efficiency Metrics
df['CO2_per_Tonne'] = df['CO2_Emissions_kg'] / df['Tonnage_Processed_tons']
df['Energy_per_Tonne'] = df['Energy_Consumption_kWh'] / df['Tonnage_Processed_tons']

col1, col2 = st.columns(2)
with col1:
    avg_co2_per_tonne = df['CO2_per_Tonne'].mean()
    st.metric(label="Avg. CO2 per Tonne of Ore", value=f"{avg_co2_per_tonne:,.2f} kg")
with col2:
    avg_energy_per_tonne = df['Energy_per_Tonne'].mean()
    st.metric(label="Avg. Energy per Tonne of Ore", value=f"{avg_energy_per_tonne:,.2f} kWh")

st.write("---")

# --- Cost Simulation ---
st.header("2. Financial Impact Simulation")
st.write("This section simulates the financial impact of operational costs and potential revenue from carbon credits.")

# --- Key Assumptions (You can explain these in your pitch) ---
cost_per_kwh = 0.12  # $0.12 per kWh
cost_per_liter = 0.90  # $0.90 per liter of diesel
carbon_credit_price = 25  # $25 per tonne of CO2

# Calculate total costs
total_energy_cost = df['Energy_Consumption_kWh'].sum() * cost_per_kwh
total_fuel_cost = df['Fuel_Consumption_L'].sum() * cost_per_liter
total_operational_cost = total_energy_cost + total_fuel_cost

# Calculate carbon credit value
total_co2_tonnes = df['CO2_Emissions_kg'].sum() / 1000
potential_carbon_credit_revenue = total_co2_tonnes * carbon_credit_price

# --- Add Chart for Cost Breakdown ---
cost_breakdown = pd.DataFrame({
    'Cost Type': ['Energy Cost', 'Fuel Cost'],
    'Total Cost ($)': [total_energy_cost, total_fuel_cost]
})
fig_cost = px.bar(cost_breakdown, x='Cost Type', y='Total Cost ($)', title='Breakdown of Total Operational Costs', color='Cost Type')
st.plotly_chart(fig_cost)

# --- Add Candlestick Chart for Daily Costs ---
df['Daily_Total_Cost'] = (df['Energy_Consumption_kWh'] * cost_per_kwh) + (df['Fuel_Consumption_L'] * cost_per_liter)
# Simulating open, high, low, close prices based on daily cost
df['Daily_Open_Cost'] = df['Daily_Total_Cost'].shift(1).fillna(df['Daily_Total_Cost'])
df['Daily_High_Cost'] = df['Daily_Total_Cost'] * 1.05
df['Daily_Low_Cost'] = df['Daily_Total_Cost'] * 0.95
df['Daily_Close_Cost'] = df['Daily_Total_Cost']

fig_candlestick = go.Figure(data=[go.Candlestick(x=df.index,
                                                open=df['Daily_Open_Cost'],
                                                high=df['Daily_High_Cost'],
                                                low=df['Daily_Low_Cost'],
                                                close=df['Daily_Close_Cost'],
                                                name="Daily Cost Volatility")])

fig_candlestick.update_layout(title='Daily Operational Cost Volatility',
                              xaxis_title='Date',
                              yaxis_title='Daily Cost ($)')

st.plotly_chart(fig_candlestick)

# Display the results
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Energy Cost", value=f"${total_energy_cost:,.0f}")
with col2:
    st.metric(label="Total Fuel Cost", value=f"${total_fuel_cost:,.0f}")
with col3:
    st.metric(label="Total Operational Cost", value=f"${total_operational_cost:,.0f}")

st.markdown(f"***Your total carbon emissions for this period were {total_co2_tonnes:,.0f} tonnes.***")
st.success(f"### Potential Carbon Credit Revenue: ${potential_carbon_credit_revenue:,.0f}")
st.write("---")

# --- Anomaly Detection ---
st.header("3. Anomaly Detection")
st.write("Identifying days with unusual energy consumption to pinpoint potential operational issues.")

# Calculate the mean and standard deviation for energy per tonne
energy_per_tonne_mean = df['Energy_per_Tonne'].mean()
energy_per_tonne_std = df['Energy_per_Tonne'].std()

# Find days that are more than 2 standard deviations away from the average
df['is_anomaly'] = (df['Energy_per_Tonne'] > energy_per_tonne_mean + 2 * energy_per_tonne_std) | \
                    (df['Energy_per_Tonne'] < energy_per_tonne_mean - 2 * energy_per_tonne_std)

anomalies = df[df['is_anomaly']]

if not anomalies.empty:
    st.warning("Potential Anomalies Detected!")
    st.dataframe(anomalies[['Tonnage_Processed_tons', 'Energy_Consumption_kWh', 'Energy_per_Tonne']])
    st.write("The table above shows days where the energy consumption was unusually high or low for the given tonnage. This may indicate a need for maintenance or process optimization.")
else:
    st.success("No significant operational anomalies detected in the dataset.")