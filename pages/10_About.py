import streamlit as st

st.title("ℹ About Team Nexus & Our Project")
st.write(f"### Problem Statement ID: SIH{st.session_state.get('problem_id', '25069')}")

st.header("The Problem")
st.write("The mining industry's environmental impact is a critical global concern. Traditional Life Cycle Assessments (LCAs) are manual, time-consuming, and outdated, making it difficult for companies to manage their sustainability in real-time. This leads to inefficient operations, high costs, and missed opportunities for environmental stewardship.")

st.header("Our Solution")
st.write("Team Nexus has developed an **AI-driven LCA tool** that automates the entire process. Our solution integrates with real-time data sources (like IoT sensors and production logs) to provide a live, predictive dashboard of a mine's environmental footprint. We transform static reports into an actionable tool for a more sustainable future.")

st.header("Our Team - Team Nexus")
st.write("We are a team of dedicated innovators focused on solving real-world problems with technology.")
st.markdown("""
* **Kartik Gupta**
* **Khushi Raghav**
* **Mohd. Hamza Khan**
* **Adhish Pradhan**
* **Jaiwin Singh Gaur**
* **Brahvish Raj Devarajan**
""")

st.header("Tech Stack")
st.write("Our project is built on a powerful, open-source technology stack designed for rapid prototyping:")
st.markdown("""
* **Language:** Python
* **Data & AI:** Pandas, NumPy, Scikit-learn
* **Web Framework:** Streamlit
* **Version Control:** Git & GitHub
""")

st.header("Future Scope")
st.write("Given more time, we would expand our project to:")
st.markdown("""
* Integrate with real-time APIs from industrial IoT devices.
* Develop a more complex deep learning model for higher prediction accuracy.
* Add more detailed LCA metrics and a full 'cradle-to-cradle' analysis.
""")