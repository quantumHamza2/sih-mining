import streamlit as st
import google.generativeai as genai

# --- API Configuration ---
# Get the API key from the secrets.toml file
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("API key not found. Please add your GOOGLE_API_KEY to the .streamlit/secrets.toml file.")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- Page Content ---
st.title("🗣️ Gemini-Powered Chatbot")
st.write("Ask me anything about mining, sustainability, or anything else!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the prompt to the Gemini API
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})