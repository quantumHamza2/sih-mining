import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import plotly.express as px

# Define the functions to load data and train the model.
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
st.title(" AI-Powered Environmental Impact Forecasting")
st.write("### Our AI model predicts future environmental impact to enable proactive sustainability management.")

df = load_and_process_data()

# Add a dropdown menu to select the prediction length
prediction_options = {
    "7 Days": 7,
    "30 Days": 30,
    "6 Months": 180
}
selected_option = st.selectbox(
    "Select a Prediction Timeframe:",
    options=list(prediction_options.keys())
)
future_days = prediction_options[selected_option]

if st.button("Generate Forecast"):
    with st.spinner("Generating prediction..."):
        future_predictions = train_predictive_model(df, future_days=future_days)
        last_date = df.index[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=future_days)
        future_df = pd.DataFrame(future_predictions, index=future_dates, columns=['Predicted CO2 Emissions (kg)'])

    # Display the results
    st.write("---")
    st.header(f"Total Forecasted CO2 Over {selected_option}")
    st.metric(label="Total Forecasted CO2", value=f"{future_df['Predicted CO2 Emissions (kg)'].sum():,.0f} kg")

    st.write("---")
    st.header("Full Historical Trend")
    st.line_chart(df['CO2_Emissions_kg'])

    st.write("---")
    st.header(f"Detailed {selected_option} Forward Projection")
    st.write("Here is the per-day forecast with markers for each day.")

    fig = px.line(future_df,
                 x=future_df.index.strftime('%a, %b %d'),
                 y='Predicted CO2 Emissions (kg)',
                 labels={'x': 'Day', 'y': 'Predicted CO2 (kg)'},
                 markers=True,  # This adds a marker for each data point
                 color_discrete_sequence=['#4B90F6'])

    st.plotly_chart(fig)

    st.write("---")
    st.header("Forecasted Data Table")
    st.dataframe(future_df)
    
st.info("💡 Select a timeframe and click 'Generate Forecast' to see the prediction.")