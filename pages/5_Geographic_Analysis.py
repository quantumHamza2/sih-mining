import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- The Data is now part of the script itself ---
data = {
    'City': ['Jharia', 'Bokaro', 'Korba', 'Talcher', 'Singareni', 'Neyveli', 'Panna', 'Joda', 'Raichur', 'Kolar', 'Bhilai', 'Ratnagiri', 'Koyilandy', 'Kalol'],
    'State': ['Jharkhand', 'Jharkhand', 'Chhattisgarh', 'Odisha', 'Telangana', 'Tamil Nadu', 'Madhya Pradesh', 'Odisha', 'Karnataka', 'Karnataka', 'Chhattisgarh', 'Maharashtra', 'Kerala', 'Gujarat'],
    'Latitude': [23.75, 23.80, 22.35, 20.95, 17.07, 11.53, 24.27, 22.12, 16.20, 12.96, 21.19, 16.98, 11.45, 22.6],
    'Longitude': [86.42, 85.75, 82.68, 85.22, 79.91, 79.48, 80.17, 85.40, 77.35, 78.27, 81.28, 73.30, 75.78, 73.45],
    'Total_Tonnage': [np.random.randint(25000, 150000) for _ in range(14)],
    'Total_CO2': [np.random.randint(10000, 75000) for _ in range(14)],
    'Primary_Mineral': ['Coal', 'Coal', 'Coal', 'Coal', 'Coal', 'Lignite', 'Diamond', 'Iron Ore', 'Gold', 'Gold', 'Iron Ore', 'Bauxite', 'Iron Ore', 'Oil']
}

df = pd.DataFrame(data)

# --- Page Content ---
st.title(" Geographic Impact Analysis (India)")
st.write("### Visualize the environmental footprint of mining across different locations.")

# --- Add a sidebar filter for states ---
st.sidebar.header("Filter by Location")
selected_state = st.sidebar.selectbox(
    "Select a State to Filter:",
    options=['All States'] + sorted(list(df['State'].unique()))
)

# Filter the dataframe based on the selected state
if selected_state != 'All States':
    filtered_df = df[df['State'] == selected_state]
else:
    filtered_df = df

# --- Display key metrics above the map ---
col1, col2 = st.columns(2)
with col1:
    total_co2_mapped = filtered_df['Total_CO2'].sum()
    st.metric(label="Total CO2 on Map", value=f"{total_co2_mapped:,.0f} kg")
with col2:
    total_tonnage_mapped = filtered_df['Total_Tonnage'].sum()
    st.metric(label="Total Tonnage on Map", value=f"{total_tonnage_mapped:,.0f} tons")

st.write("---")

# Create the interactive scatter map with a beautiful theme
fig = px.scatter_geo(filtered_df, lat='Latitude', lon='Longitude',
                     hover_name='City',
                     hover_data={
                        'City': False, # Hide default hover city
                        'State': True,
                        'Primary_Mineral': True,
                        'Total_CO2': ':.0f kg',
                        'Total_Tonnage': ':.0f tons'
                     },
                     size='Total_CO2', # Use CO2 as a size indicator for visual impact
                     color='Primary_Mineral', # Color by the type of mineral
                     projection="natural earth",
                     title='Mining Activity by City',
                     scope='asia',
                     center={'lat': 22.0, 'lon': 78.0},
                     width=800, height=600,
                     template='plotly_dark') # Keep dark theme for overall chart elements

# Update the layout to focus on India with white outlines
fig.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="White", # Changed to White
    showsubunits=True, subunitcolor="Gray",   # Changed to Gray for internal state borders
    lataxis_range=[8, 38], lonaxis_range=[68, 98],
    # Dark land color for contrast with white borders
    showland=True,
    landcolor='rgb(60, 60, 60)', # Darker land color
    bgcolor='black' # Keep overall background black
)

st.plotly_chart(fig)

st.info("The **size** of each circle represents the total CO2 emissions, and the **color** represents the primary mineral mined.")

st.write("---")
st.header("Data Table")
st.dataframe(filtered_df)