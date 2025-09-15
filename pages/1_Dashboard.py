import streamlit as st
import pandas as pd
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
    df['Water_Impact_m3'] = df['Water_Usage_m3'] * 1.2
    df['Land_Impact_m2'] = df['Tonnage_Processed_tons'] * 0.005
    return df

# --- Page Content ---
st.title("📊 Real-Time Mining Sustainability Dashboard")
st.markdown("### An overview of key environmental performance indicators.")

# Load the original, unfiltered data here first
df = load_and_process_data()

# Now, we can create the filter using values from the loaded data
st.sidebar.header("Data Filter")
min_tonnage = st.sidebar.slider(
    'Minimum Tonnage Processed',
    min_value=int(df['Tonnage_Processed_tons'].min()),
    max_value=int(df['Tonnage_Processed_tons'].max()),
    value=int(df['Tonnage_Processed_tons'].min())
)

# Apply the filter to the data
filtered_df = df[df['Tonnage_Processed_tons'] >= min_tonnage]

# Check if the filtered data is empty before displaying anything
if filtered_df.empty:
    st.warning("No data matches the selected filter. Please adjust the slider.")
else:
    # --- Display all metrics and charts using the filtered_df ---
    
    # Use columns to display key metrics side-by-side
    col1, col2, col3 = st.columns(3)
    with col1:
        total_co2 = filtered_df['CO2_Emissions_kg'].sum()
        st.metric(label="Total CO2 Emissions", value=f"{total_co2:,.0f} kg")
    with col2:
        total_water = filtered_df['Water_Usage_m3'].sum()
        st.metric(label="Total Water Usage", value=f"{total_water:,.0f} m³")
    with col3:
        avg_co2_daily = filtered_df['CO2_Emissions_kg'].mean()
        st.metric(label="Average Daily CO2", value=f"{avg_co2_daily:,.0f} kg")

    st.write("---")

    # Use a selectbox to allow users to choose a metric to visualize
    st.header("Historical Trends")
    selected_metric = st.selectbox(
        "Select a Metric to View its Trend:",
        ['CO2_Emissions_kg', 'Water_Usage_m3', 'Energy_Consumption_kWh']
    )
    st.line_chart(filtered_df[selected_metric])
    
    st.write("---")
    st.header("What-If Analysis")
    st.markdown("Adjust the sliders below to see the real-time impact on environmental metrics.")

    # Use a slider to get user input for a change in energy consumption
    energy_change_percent = st.slider(
        'Change in Energy Consumption (%)',
        min_value=-50, max_value=50, value=0, step=5
    )

    # Get the original average daily energy consumption
    original_avg_energy = filtered_df['Energy_Consumption_kWh'].mean()

    # Calculate the new average based on the slider
    new_avg_energy = original_avg_energy * (1 + energy_change_percent / 100)

    # Apply the same change to the average daily CO2
    original_avg_co2 = filtered_df['CO2_Emissions_kg'].mean()
    new_avg_co2 = original_avg_co2 * (1 + energy_change_percent / 100)

    # Display the results
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Original Avg. Daily Energy", value=f"{original_avg_energy:,.0f} kWh")
        st.metric(label="New Avg. Daily Energy", value=f"{new_avg_energy:,.0f} kWh")
    with col2:
        st.metric(label="Original Avg. Daily CO2", value=f"{original_avg_co2:,.0f} kg")
        st.metric(label="New Avg. Daily CO2", value=f"{new_avg_co2:,.0f} kg")

    st.info("This analysis shows how a simple change in energy efficiency can directly impact your carbon footprint.")
    st.write("---")

    # Use an expander to show a detailed data table
    with st.expander("Click here to view the raw data"):
        st.dataframe(filtered_df)