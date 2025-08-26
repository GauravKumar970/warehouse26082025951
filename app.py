
import streamlit as st
import pandas as pd
import google.generativeai as genai
from data_agent import generate_warehouse_data
from inventory_agent import perform_abc_analysis
from slotting_agent import recommend_slotting
from kpi_agent import calculate_kpis

# Configure Gemini API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except KeyError:
    st.warning("Gemini API key not found. Please add it to your Streamlit secrets.")
    model = None

st.title("Smart Space Management: AI-Driven Warehouse Optimization")
st.markdown("Click 'Run Optimization' to simulate real-time warehouse data and generate insights.")

if st.button("Run Optimization"):
    df_raw = generate_warehouse_data()
    df_analyzed = perform_abc_analysis(df_raw)
    df_optimized = recommend_slotting(df_analyzed)
    total_volume = 1000000
    kpis = calculate_kpis(df_raw, df_optimized, total_volume)

    st.subheader("Key Performance Indicators")
    for kpi, value in kpis.items():
        st.markdown(f"**{kpi}:** {value}")
        if kpi == "Storage Utilization Rate":
            st.markdown("F4CC *Recommendation:* Ensure high-demand items are prioritized. A very high rate may indicate overstocking.")
        elif kpi == "Inventory Consolidation Index":
            st.markdown("F4CC *Recommendation:* Consolidate fragmented SKUs to reduce retrieval time and improve space usage.")
        elif kpi == "Average Pick Time":
            st.markdown("F4CC *Recommendation:* Reduce pick time by placing fast-moving items closer to picking zones.")
        elif kpi == "Slotting Accuracy":
            st.markdown("F4CC *Recommendation:* Improve slotting logic to ensure high-turnover items are in optimal zones.")
        elif kpi == "Space Cost per Unit Stored":
            st.markdown("F4CC *Recommendation:* Lower cost per unit by optimizing layout and reducing long-tail SKUs.")

    st.subheader("AI-Driven Recommendation Summary")
    if model:
        prompt = f"Based on the following KPI analysis: {kpis}. Provide a detailed recommendation for warehouse optimization considering ABC classification, slotting, consolidation, and cost efficiency."
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Gemini API error: {e}")
    else:
        st.info("Gemini summary not available due to missing API key.")

    with st.expander("Show Agent Interactions"):
        st.markdown("**Data Agent:** Simulates real-time inventory data")
        st.markdown("**Inventory Agent:** Performs ABC analysis")
        st.markdown("**Slotting Agent:** Recommends optimal placement")
        st.markdown("**KPI Agent:** Calculates performance metrics")
