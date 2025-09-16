import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_and_process_data(file_path='mining_data.csv'):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    CO2_PER_KWH = 0.5
    CO2_PER_LITER_DIESEL = 2.7
    df['CO2_Emissions_kg'] = (df['Energy_Consumption_kWh'] * CO2_PER_KWH) + (df['Fuel_Consumption_L'] * CO2_PER_LITER_DIESEL)
    return df

st.title(" The Story Our Data Tells")
st.write("### A narrative look at key events and insights from our operational data.")

df = load_and_process_data()

st.write("---")

# Find the day with the highest emissions
highest_emission_day = df.loc[df['CO2_Emissions_kg'].idxmax()]
st.header("The Most Polluting Day ")
st.markdown(f"""
Our data shows that the day with the highest carbon emissions would be **{highest_emission_day.name.strftime('%B %d, %Y')}**.
On this day, the mine emitted a total of **{highest_emission_day['CO2_Emissions_kg']:,.0f} kg of CO2**.
""")

st.write("---")

# Find the month with the lowest average emissions
df['Month'] = df.index.month
monthly_avg_emissions = df.groupby('Month')['CO2_Emissions_kg'].mean()
lowest_emission_month = monthly_avg_emissions.idxmin()
st.header("The Most Efficient Month ")
st.markdown(f"""
The most efficient month for the mine would be **{pd.to_datetime(str(lowest_emission_month), format='%m').strftime('%B')}**,
with an average of only **{monthly_avg_emissions.min():,.0f} kg of CO2** per day.
""")

st.write("---")

# Find the most productive day
highest_tonnage_day = df.loc[df['Tonnage_Processed_tons'].idxmax()]
st.header("The Most Productive Day ")
st.markdown(f"""
The mine had its most productive day on **{highest_tonnage_day.name.strftime('%B %d, %Y')}**,
processing a total of **{highest_tonnage_day['Tonnage_Processed_tons']:,.0f} tons of ore**.
""")

st.write("---")

st.info("This kind of data storytelling can help managers celebrate success and pinpoint specific days that need further analysis to improve efficiency.")