import streamlit as st

st.set_page_config(
    page_title="Team Nexus - SIH Project",
    page_icon="🤖",
    layout="wide",
)

# --- This is the content for your main 'app' page ---
st.title("🌱 AI-Driven LCA Tool for Mining Sustainability")
st.write("### A proactive solution for environmental stewardship in the mining industry.")

st.write("---")

st.header("The Challenge")
st.markdown("Traditional Life Cycle Assessments (LCAs) are manual, time-consuming, and expensive. They provide a static, historical view of environmental impact, making it difficult for mining companies to respond in real-time to sustainability challenges.")

st.header("Our Solution")
st.markdown("""
Team Nexus has developed an innovative tool that leverages **AI and real-time data** to provide a dynamic, predictive dashboard of a mine's environmental footprint.
* **Automated Data Ingestion:** We integrate data from IoT sensors, production logs, and supply chains.
* **Real-time LCA Metrics:** We automatically calculate key metrics like CO2 emissions and water usage.
* **Predictive AI:** Our machine learning model forecasts future environmental impacts, enabling proactive decision-making.
""")

st.write("---")

st.info("👈 Choose a page from the sidebar to explore our project features and see the live demo.")