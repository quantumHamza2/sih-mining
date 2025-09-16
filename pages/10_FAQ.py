import streamlit as st

st.title(" Frequently Asked Questions")
st.write("A quick guide to understanding our project, its technology, and its impact.")

st.write("---")

# Question 1
with st.expander("What is the core problem your project solves?"):
    st.markdown("""
    Our project solves the problem of **outdated and inefficient environmental tracking** in the mining industry. Traditional methods, like manual Life Cycle Assessments (LCAs), are time-consuming and don't provide real-time data, making it impossible for companies to react quickly to sustainability challenges.
    """)

# Question 2
with st.expander("What is a Life Cycle Assessment (LCA)?"):
    st.markdown("""
    An LCA is a method for measuring the total environmental impact of a product or process, from "cradle to grave." For a mine, this means tracking all the energy, water, and waste used from the moment raw ore is extracted until the final product is delivered.
    """)

# Question 3
with st.expander("What is a Digital Twin?"):
    st.markdown("""
    A digital twin is a virtual copy of a physical object or system, like a mine. Our project creates a digital twin that is fed with real-time data (e.g., from sensors). This allows us to monitor the mine's environmental footprint live and simulate the impact of future changes.
    """)

# Question 4
with st.expander("How does your AI work?"):
    st.markdown("""
    Our project uses a machine learning model that is trained on historical operational data (like energy and fuel consumption). It learns the relationship between these activities and the resulting environmental impact. This allows it to make accurate **predictions** about future emissions.
    """)

# Question 5
with st.expander("Where does your data come from?"):
    st.markdown("""
    For this demo, we use a synthetic, or simulated, dataset that we created based on typical mining operations. In a real-world scenario, our system would connect to real-time data from **IoT sensors**, production logs, and supply chain records.
    """)

# Question 6
with st.expander("What is the biggest benefit of your tool?"):
    st.markdown("""
    The biggest benefit is **real-time insight**. Instead of waiting months for a report, a mining company can see their environmental impact instantly and use our predictive analysis to make proactive decisions that reduce their carbon footprint and save money.
    """)

# --- Add this note for your pitch
st.write("---")
st.info("💡 **For the judges:** We chose this FAQ format to ensure all our key points are delivered clearly, without any risk of a live demo issue.")