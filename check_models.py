import google.generativeai as genai
import streamlit as st

# Get the API key from the secrets.toml file
if "GOOGLE_API_KEY" not in st.secrets:
    print("API key not found. Please add your GOOGLE_API_KEY to the .streamlit/secrets.toml file.")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Print the available models
for m in genai.list_models():
  print(f"{m.name} - {m.description}")