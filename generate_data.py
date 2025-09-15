import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Configuration for your dataset ---
START_DATE = datetime(2025, 1, 1)  # Starting date for your data
NUM_DAYS = 730  # Number of days to simulate (e.g., one year)
BASE_TONNAGE = 5000  # Average daily tonnage of ore processed
BASE_WATER_USAGE = 1500  # Average daily water usage in cubic meters
BASE_ENERGY_CONSUMPTION = 8000  # Average daily energy consumption in kWh
BASE_FUEL_CONSUMPTION = 1000  # Average daily fuel consumption in Liters

# --- Conversion Factors (LCA calculations) ---
CO2_PER_KWH = 0.5  # kg CO2 per kWh of electricity
CO2_PER_LITER_DIESEL = 2.7  # kg CO2 per liter of diesel
WATER_IMPACT_FACTOR = 1.2
LAND_IMPACT_FACTOR = 0.005

# --- Generate the core time-series data ---
dates = [START_DATE + timedelta(days=i) for i in range(NUM_DAYS)]
tonnage = np.array([BASE_TONNAGE + random.uniform(-1000, 1000) for _ in range(NUM_DAYS)])
tonnage[tonnage < 0] = 0

energy_consumption = BASE_ENERGY_CONSUMPTION + (tonnage / BASE_TONNAGE) * 2000 + np.random.normal(0, 500, NUM_DAYS)
water_usage = BASE_WATER_USAGE + (tonnage / BASE_TONNAGE) * 500 + np.random.normal(0, 200, NUM_DAYS)
fuel_consumption = BASE_FUEL_CONSUMPTION + (tonnage / BASE_TONNAGE) * 300 + np.random.normal(0, 100, NUM_DAYS)

# --- Create the DataFrame and perform LCA calculations ---
data = {
    'Date': dates,
    'Tonnage_Processed_tons': tonnage,
    'Energy_Consumption_kWh': energy_consumption.round(2),
    'Water_Usage_m3': water_usage.round(2),
    'Fuel_Consumption_L': fuel_consumption.round(2)
}
df = pd.DataFrame(data)

df['CO2_Emissions_kg'] = (df['Energy_Consumption_kWh'] * CO2_PER_KWH) + (df['Fuel_Consumption_L'] * CO2_PER_LITER_DIESEL)
df['Water_Impact_m3'] = df['Water_Usage_m3'] * WATER_IMPACT_FACTOR
df['Land_Impact_m2'] = df['Tonnage_Processed_tons'] * LAND_IMPACT_FACTOR

# --- Save the dataset to a CSV file ---
df.to_csv('mining_data.csv', index=False)

print("Dataset 'mining_data.csv' created successfully!")
print(f"It contains data for {NUM_DAYS} days.")
print("\nHere's a preview of the first 5 rows:")
print(df.head())