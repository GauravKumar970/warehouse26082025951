import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import io

# Import AI agents
from data_agent import generate_warehouse_data
from inventory_agent import perform_abc_analysis
from slotting_agent import recommend_slotting
from kpi_agent import calculate_kpis
from recommendation_agent import generate_kpi_recommendations

# --- Initial Page Load ---
st.title("Smart Space Management: AI-Driven Warehouse Optimization")
st.write("Welcome to the Warehouse Optimization Dashboard. All AI agents are ready to work.")

# Initialize session state for data
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = generate_warehouse_data()
    st.session_state.df_analyzed = perform_abc_analysis(st.session_state.df_raw)
    st.session_state.df_optimized = recommend_slotting(st.session_state.df_analyzed)
    st.session_state.kpis = calculate_kpis(st.session_state.df_raw, st.session_state.df_optimized)
    st.session_state.recommendations = {}
    st.session_state.summary = ""

st.subheader("Current Key Performance Indicators")
for k, v in st.session_state.kpis.items():
    st.write(f"**{k.replace('_', ' ').title()}**: {v}")

st.subheader("Contributing AI Agents")
st.markdown(
    "The following AI agents are active and contribute to the decision-making process: "
    "**Data Agent**, **Inventory Agent**, **Slotting Agent**, **KPI Agent**, and **Recommendation Agent**."
)

st.subheader("Optimized Warehouse Layout Recommendations")
st.dataframe(st.session_state.df_optimized[['Product_ID', 'ABC_Category', 'Daily_Demand', 'Current_Location', 'New_Location']])


# --- Gemini API Configuration ---
# Ensure your Streamlit app has the GEMINI_API_KEY as a secret
# Go to "Manage app" > "Settings" > "Secrets" in Streamlit Cloud
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_summary_with_gemini(kpis, recommendations):
    prompt = f"""
    You are an AI-powered warehouse management consultant. Your task is to generate a comprehensive, professional summary based on the provided Key Performance Indicators (KPIs) and recommendations from an AI-driven warehouse optimization run.

    Here are the KPI results:
    {kpis}

    Here are the actionable recommendations for each KPI:
    {recommendations}

    Please write a detailed report that:
    1. Summarizes the overall performance of the warehouse.
    2. Highlights the key successes of the optimization, especially in improving picking efficiency and space utilization.
    3. Provides clear, actionable next steps based on the recommendations.
    4. Concludes with a statement on the value of a data-driven approach to warehouse management.
    The summary should be professional, insightful, and formatted for easy readability.
    """
    response = model.generate_content(prompt)
    return response.text

# --- Button and Logic for Optimization Run ---
st.markdown("---")
if st.button("Run Optimization"):
    # Create a simple progress bar
    progress_bar = st.progress(0)

    # Step 1: Generate Raw Data
    with st.spinner('Generating raw warehouse data...'):
        st.session_state.df_raw = generate_warehouse_data()
    progress_bar.progress(25)

    # Step 2: Perform ABC Analysis
    with st.spinner('Performing ABC analysis on inventory...'):
        st.session_state.df_analyzed = perform_abc_analysis(st.session_state.df_raw)
    progress_bar.progress(50)

    # Step 3: Recommend Slotting
    with st.spinner('Recommending optimized slotting locations...'):
        st.session_state.df_optimized = recommend_slotting(st.session_state.df_analyzed)
    progress_bar.progress(75)

    # Step 4: Calculate KPIs
    with st.spinner('Calculating key performance indicators...'):
        st.session_state.kpis = calculate_kpis(st.session_state.df_raw, st.session_state.df_optimized)
    progress_bar.progress(85)
    
    # Step 5: Generate Recommendations
    with st.spinner('Generating recommendations...'):
        st.session_state.recommendations = generate_kpi_recommendations(st.session_state.kpis)
    progress_bar.progress(95)

    # Step 6: Generate Summary with Gemini
    with st.spinner('Compiling a detailed summary with Gemini...'):
        st.session_state.summary = generate_summary_with_gemini(st.session_state.kpis, st.session_state.recommendations)
    progress_bar.progress(100)
    st.success('Optimization complete!')
    st.rerun()

# --- Post-Optimization Display (Reloads on button click) ---
if st.session_state.summary:
    st.subheader("Detailed Recommendations")
    for k, v in st.session_state.recommendations.items():
        st.write(f"**{k.replace('_', ' ').title()}**: {v}")

    st.subheader("Gemini-Powered Executive Summary")
    st.write(st.session_state.summary)

    # Create a download button for the summary
    buffer = io.StringIO(st.session_state.summary)
    st.download_button(
        label="Download Summary as Text File",
        data=buffer.getvalue(),
        file_name="warehouse_optimization_summary.txt",
        mime="text/plain"
    )
