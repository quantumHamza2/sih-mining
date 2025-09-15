import streamlit as st

st.set_page_config(
    page_title="Team Nexus - SIH Project",
    page_icon="🤖",
    layout="wide",
)
st.sidebar.title("Navigation")
st.sidebar.write("Choose a page from the sidebar to view our project.")

# This simple code is all that's needed. Streamlit automatically
# detects and displays the pages in the 'pages' directory.