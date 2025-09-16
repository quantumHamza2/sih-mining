import streamlit as st
import pandas as pd
import plotly.express as px

# Define the function to load and process data
@st.cache_data
def load_and_process_data(file_path='mining_data.csv'):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    CO2_PER_KWH = 0.5
    CO2_PER_LITER_DIESEL = 2.7
    df['CO2_Emissions_kg'] = (df['Energy_Consumption_kWh'] * CO2_PER_KWH) + (df['Fuel_Consumption_L'] * CO2_PER_LITER_DIESEL)
    df['Water_Impact_m3'] = df['Water_Usage_m3'] * 1.2
    df['Land_Impact_m2'] = df['Tonnage_Processed_tons'] * 0.005
    return df

# --- Page Content ---
st.title(" Detailed Life Cycle Analysis")
st.write("### A granular breakdown of environmental impacts across the mining value chain.")

df = load_and_process_data()

st.write("### Impact Contribution Breakdown")
impact_data = {
    'Impact Category': ['CO2 Emissions', 'Water Usage', 'Land Use'],
    'Value': [df['CO2_Emissions_kg'].sum(), df['Water_Usage_m3'].sum(), df['Land_Impact_m2'].sum()]
}
impact_df = pd.DataFrame(impact_data)
fig = px.pie(impact_df, values='Value', names='Impact Category', title='Total Environmental Footprint Breakdown')
st.plotly_chart(fig)

st.write("---")
st.write("### Correlation: Tonnage vs. Emissions")
st.write("This scatter plot shows the direct relationship between the amount of ore processed and the resulting CO2 emissions.")
fig2 = px.scatter(df, x='Tonnage_Processed_tons', y='CO2_Emissions_kg', trendline='ols')
st.plotly_chart(fig2)

st.write("---")
st.write("### Raw Data Table")
st.dataframe(df)