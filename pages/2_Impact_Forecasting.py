import streamlit as st
import pandas as pd
import numpy as np  # <-- The missing line
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Define the functions to load data and train the model.
# These are the same functions from your original app.py.
@st.cache_data
def load_and_process_data(file_path='mining_data.csv'):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    CO2_PER_KWH = 0.5
    CO2_PER_LITER_DIESEL = 2.7
    df['CO2_Emissions_kg'] = (df['Energy_Consumption_kWh'] * CO2_PER_KWH) + (df['Fuel_Consumption_L'] * CO2_PER_LITER_DIESEL)
    return df

def train_predictive_model(df, target='CO2_Emissions_kg', future_days=7):
    """Trains a simple regression model to predict future emissions with variability."""
    
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
    
    energy_std = df['Energy_Consumption_kWh'].std()
    fuel_std = df['Fuel_Consumption_L'].std()

    for i in range(future_days):
        future_data.iloc[i]['Day_of_Year'] = (last_row_data['Day_of_Year'] + i + 1) % 365
        future_data.iloc[i]['Month'] = (last_row_data['Month'] + ((last_row_data['Day_of_Year'] + i) // 30)) % 12
        
        future_data.iloc[i]['Energy_Consumption_kWh'] = last_row_data['Energy_Consumption_kWh'] + np.random.normal(0, energy_std * 0.1)
        future_data.iloc[i]['Fuel_Consumption_L'] = last_row_data['Fuel_Consumption_L'] + np.random.normal(0, fuel_std * 0.1)
    
    future_predictions = model.predict(future_data)
    return future_predictions

# --- Page Content ---
st.title("🔮 AI-Powered Environmental Impact Forecasting")
st.write("### Our AI model predicts future environmental impact to enable proactive sustainability management.")

df = load_and_process_data()

st.write("### 7-Day Forward Projection")
future_predictions = train_predictive_model(df)
last_date = df.index[-1]
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)
future_df = pd.DataFrame(future_predictions, index=future_dates, columns=['Predicted CO2 Emissions (kg)'])

st.line_chart(future_df)
st.dataframe(future_df)

st.write("---")
st.write("#### How it works:")
st.info("Our machine learning model is trained on historical data to identify patterns between operational metrics (like energy and fuel consumption) and environmental outputs. This allows us to forecast future emissions based on current trends, giving stakeholders a proactive tool to manage their environmental footprint.")