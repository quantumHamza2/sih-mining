import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

# --- NEW FUNCTION to parse dates from the prompt ---
def get_date_from_prompt(prompt, df_dates):
    """
    Tries to find a date in the user's prompt and returns it as a datetime object.
    Supports a few simple formats.
    """
    prompt_words = prompt.split()
    for word in prompt_words:
        try:
            date_str = pd.to_datetime(word, format='%Y-%m-%d', errors='coerce')
            if pd.notna(date_str):
                return date_str
        except:
            pass
    # Simple check for month/day format
    try:
        date_str = pd.to_datetime(prompt, errors='coerce')
        if pd.notna(date_str) and date_str in df_dates:
            return date_str
    except:
        pass
    return None

# --- Page Content ---
st.title("🤖 AI-Powered Q&A Chatbot")
st.write("Ask me a question about the dashboard data.")

# Load the data
df = load_and_process_data()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ""
        prompt_lower = prompt.lower()
        
        # --- Check for specific date queries first ---
        date_query = get_date_from_prompt(prompt, df.index)
        if date_query is not None and "co2" in prompt_lower:
            if date_query in df.index:
                co2_on_date = df.loc[date_query, 'CO2_Emissions_kg']
                response = f"On **{date_query.strftime('%B %d, %Y')}**, the CO2 emissions were approximately **{co2_on_date:,.0f} kg**."
            else:
                response = "I'm sorry, I don't have data for that specific date. Please try another date within our dataset."
        elif date_query is not None and "water" in prompt_lower:
            if date_query in df.index:
                water_on_date = df.loc[date_query, 'Water_Usage_m3']
                response = f"On **{date_query.strftime('%B %d, %Y')}**, the water usage was approximately **{water_on_date:,.0f} m³**."
            else:
                response = "I'm sorry, I don't have data for that specific date. Please try another date within our dataset."
        
        # --- Now, check for user-friendly explanations ---
        elif "what is" in prompt_lower or "explain" in prompt_lower or "tell me about" in prompt_lower:
            if "lca" in prompt_lower or "life cycle" in prompt_lower:
                response = "LCA is like tracking a product's footprint from when it's born until it's gone. For a mine, that means looking at all the energy, water, and waste it uses to get a metal from the ground and turn it into something useful."
            elif "carbon footprint" in prompt_lower or "emissions" in prompt_lower or "co2" in prompt_lower:
                response = "Carbon footprint is like the total amount of pollution we make. We measure it in CO2 because that's a common type of air pollution that can be easily tracked."
            elif "digital twin" in prompt_lower:
                response = "A digital twin is a living, breathing digital copy of something real, like a factory or a mine. It lets us test ideas and see what will happen without touching the real thing."
            else:
                response = "I'm sorry, I can only provide simple explanations for LCA, carbon footprint, or a digital twin."

        # --- Now, check for specific data queries (totals and averages) ---
        elif "co2" in prompt_lower and ("total" in prompt_lower or "sum" in prompt_lower):
            total_co2 = df['CO2_Emissions_kg'].sum()
            response = f"The total CO2 emissions for the entire period are approximately {total_co2:,.0f} kg."
        elif "co2" in prompt_lower and ("average" in prompt_lower or "avg" in prompt_lower):
            avg_co2 = df['CO2_Emissions_kg'].mean()
            response = f"The average daily CO2 emissions are approximately {avg_co2:,.0f} kg."
        elif "water" in prompt_lower and ("total" in prompt_lower or "sum" in prompt_lower):
            total_water = df['Water_Usage_m3'].sum()
            response = f"The total water usage for the entire period is approximately {total_water:,.0f} m³."
        elif "tonnage" in prompt_lower or "processed" in prompt_lower:
            response = "Tonnage processed refers to the amount of raw ore extracted and processed by the mine in metric tons."
        
        # --- Default error message ---
        else:
            response = "I'm sorry, I don't understand that question. Try asking me for **total** or **average** metrics, or a specific date like **'2025-01-05'**."
            
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})