import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# --- Configuration for LCA Factors ---
CO2_PER_KWH = 0.5  # kg CO2 per kWh
CO2_PER_LITER_DIESEL = 2.7  # kg CO2 per liter

# --- Function to load and process data ---
@st.cache_data
def load_and_process_data(file_path='mining_data.csv'):
    """Loads data, performs LCA calculations, and returns a processed DataFrame."""
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    df['CO2_Emissions_kg'] = (df['Energy_Consumption_kWh'] * CO2_PER_KWH) + (df['Fuel_Consumption_L'] * CO2_PER_LITER_DIESEL)
    
    return df

# --- Build the Predictive Model (The 'AI' part) ---
def train_predictive_model(df, target='CO2_Emissions_kg', future_days=7):
    """Trains a simple regression model to predict future emissions."""
    
    df['Day_of_Year'] = df.index.dayofyear
    df['Month'] = df.index.month
    
    features = ['Energy_Consumption_kWh', 'Fuel_Consumption_L', 'Day_of_Year', 'Month']
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    model = LinearRegression()
    model.fit(X_train, y_train)

    last_row_data = X.iloc[-1]
    future_data = pd.DataFrame(index=range(future_days), columns=features)
    for i in range(future_days):
        future_data.iloc[i]['Day_of_Year'] = (last_row_data['Day_of_Year'] + i + 1) % 365
        future_data.iloc[i]['Month'] = (last_row_data['Month'] + ((last_row_data['Day_of_Year'] + i) // 30)) % 12
        # For simplicity, assume future energy and fuel consumption remain similar to the last known value
        future_data.iloc[i]['Energy_Consumption_kWh'] = last_row_data['Energy_Consumption_kWh']
        future_data.iloc[i]['Fuel_Consumption_L'] = last_row_data['Fuel_Consumption_L']
    
    future_predictions = model.predict(future_data)
    return future_predictions

# --- Build the Streamlit Dashboard ---
def main():
    st.title('AI-Driven LCA Tool for Mining Sustainability')
    st.write('### Real-time Environmental Impact Dashboard')

    df = load_and_process_data()

    total_co2 = df['CO2_Emissions_kg'].sum()
    avg_co2_daily = df['CO2_Emissions_kg'].mean()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total CO2 Emissions", value=f"{total_co2:,.0f} kg")
    with col2:
        st.metric(label="Average Daily CO2", value=f"{avg_co2_daily:,.0f} kg")

    st.write('---')
    
    st.write("### Historical CO2 Emissions Trend")
    st.line_chart(df['CO2_Emissions_kg'])

    st.write("### 7-Day Forward Projection (Powered by AI)")
    future_predictions = train_predictive_model(df)
    
    last_date = df.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)
    future_df = pd.DataFrame(future_predictions, index=future_dates, columns=['Predicted CO2 Emissions (kg)'])
    
    st.line_chart(future_df)
    st.dataframe(future_df)

if __name__ == '__main__':
    main()