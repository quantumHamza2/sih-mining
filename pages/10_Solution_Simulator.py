import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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

# --- Page Content ---
st.title("Solution Simulator")
st.write("### Choose a solution to see its simulated impact on a key metric.")

df = load_and_process_data()

# Initialize session state for the button click
if 'solution_selected' not in st.session_state:
    st.session_state.solution_selected = 'none'

# Create the buttons with a cleaner layout
st.write("---")
st.markdown("#### **Choose an Action:**")
col1, col2, col3, col4 = st.columns(4, gap="small") # Use columns for uniform size
with col1:
    if st.button("Solar Energy", use_container_width=True):
        st.session_state.solution_selected = 'solar'
with col2:
    if st.button("Fleet Electrification", use_container_width=True):
        st.session_state.solution_selected = 'fleet'
with col3:
    if st.button("Water System", use_container_width=True):
        st.session_state.solution_selected = 'water'
with col4:
    if st.button("Process Optimization", use_container_width=True):
        st.session_state.solution_selected = 'optimize'

# Create a container for the chart and metrics
chart_and_metrics = st.container()

if st.session_state.solution_selected == 'none':
    st.info("Click one of the buttons above to see a solution's impact.")
else:
    # --- Simulate the impact based on the button clicked ---
    simulated_df = df.copy()
    metric_to_show = 'CO2_Emissions_kg'
    impact_percent = 0.0
    impact_description = ""
    simulated_df['Scenario'] = 'Original Data'

    if st.session_state.solution_selected == 'solar':
        impact_percent = 0.30
        impact_description = "Switching to solar energy"
        simulated_df['Simulated Impact'] = simulated_df[metric_to_show] * (1 - impact_percent)
    elif st.session_state.solution_selected == 'fleet':
        impact_percent = 0.15
        impact_description = "Electrifying the vehicle fleet"
        simulated_df['Simulated Impact'] = simulated_df[metric_to_show] * (1 - impact_percent)
    elif st.session_state.solution_selected == 'water':
        impact_percent = 0.50
        impact_description = "Implementing a closed-loop water system"
        metric_to_show = 'Water_Wastage_m3'
        simulated_df['Simulated Impact'] = simulated_df[metric_to_show] * (1 - impact_percent)
    elif st.session_state.solution_selected == 'optimize':
        impact_percent = 0.10
        impact_description = "Optimizing a key process"
        simulated_df['Simulated Impact'] = simulated_df[metric_to_show] * (1 - impact_percent)

    # Create a combined DataFrame for the animated chart
    simulated_df_new = simulated_df.copy()
    simulated_df_new[metric_to_show] = simulated_df_new['Simulated Impact']
    simulated_df_new['Scenario'] = 'Simulated Impact'
    
    # Combine the dataframes and plot
    combined_df = pd.concat([simulated_df, simulated_df_new])
    
    with chart_and_metrics:
        st.success(f"Simulating a **{impact_percent * 100:.0f}% reduction** from **{impact_description}**.")
        st.header("Simulated Impact")
        
        # Create an animated chart
        fig = px.line(combined_df, x=combined_df.index, y=metric_to_show, color='Scenario',
                      title=f"Original vs. Simulated Impact on {metric_to_show.replace('_', ' ')}",
                      labels={'Value': metric_to_show, 'Date': 'Date'},
                      color_discrete_map={'Original Data': 'grey', 'Simulated Impact': '#228B22'}) # Changed color to a trading green

        fig.update_layout(transition_duration=1000)
        
        st.plotly_chart(fig)