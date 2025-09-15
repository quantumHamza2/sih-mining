import pandas as pd
import numpy as np
import requests
import io

# New, working URL for a public dataset of Indian cities with lat/lon
url = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/cities.csv"

def generate_mining_data(cities_df):
    """
    Generates simulated mining data for a subset of the provided cities.
    """
    # Filter for cities in India
    india_cities = cities_df[cities_df['country_code'] == 'IN']
    
    # Select a random subset of cities to have mining data
    mining_cities = india_cities.sample(n=300, random_state=42)

    # Add simulated data columns
    mining_cities['Total_Tonnage'] = np.random.randint(10000, 150000, size=len(mining_cities))
    mining_cities['Total_CO2'] = mining_cities['Total_Tonnage'] * np.random.uniform(0.5, 0.9, size=len(mining_cities))
    mining_cities['Primary_Mineral'] = np.random.choice(
        ['Coal', 'Iron Ore', 'Gold', 'Bauxite', 'Copper', 'Diamond'],
        size=len(mining_cities)
    )
    
    # Select and rename the relevant columns for your map
    final_df = mining_cities[['name', 'state_name', 'latitude', 'longitude', 'Total_Tonnage', 'Total_CO2', 'Primary_Mineral']]
    final_df.rename(columns={'name': 'City', 'state_name': 'State'}, inplace=True)
    
    return final_df

# Download the city data
try:
    response = requests.get(url)
    response.raise_for_status() # Raise an exception for bad status codes
    # Use io.StringIO to read the content as a string
    cities_data = pd.read_csv(io.StringIO(response.text))
    
    # Generate the simulated mining data
    final_df = generate_mining_data(cities_data)
    
    # Save the combined data to a new CSV
    final_df.to_csv('indian_mining_data.csv', index=False)
    
    print("Updated geospatial data with way more cities created successfully!")
    print(f"It contains {len(final_df)} data points.")

except requests.exceptions.RequestException as e:
    print(f"Error downloading the city data: {e}")
    print("Using fallback data...")
    # Fallback to the small, hardcoded dataset if download fails
    fallback_data = {
        'City': ['Jharia', 'Bokaro', 'Korba', 'Talcher', 'Singareni', 'Neyveli'],
        'State': ['Jharkhand', 'Jharkhand', 'Chhattisgarh', 'Odisha', 'Telangana', 'Tamil Nadu'],
        'Latitude': [23.75, 23.80, 22.35, 20.95, 17.07, 11.53],
        'Longitude': [86.42, 85.75, 82.68, 85.22, 79.91, 79.48],
        'Total_Tonnage': np.random.randint(10000, 150000, size=6),
        'Total_CO2': np.random.randint(10000, 75000, size=6),
        'Primary_Mineral': np.random.choice(['Coal', 'Iron Ore', 'Gold', 'Bauxite', 'Copper', 'Diamond'], size=6)
    }
    pd.DataFrame(fallback_data).to_csv('indian_mining_data.csv', index=False)