import streamlit as st
import pandas as pd
import google.generativeai as genai
import io
import plotly.express as px

# Import AI agents
from data_agent import generate_warehouse_data
from inventory_agent import perform_abc_analysis
from slotting_agent import recommend_slotting
from kpi_agent import calculate_kpis
from recommendation_agent import generate_kpi_recommendations

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Smart Warehouse Optimization for CTO")

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .kpi-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dcdcdc;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .agent-box {
        background-color: #e6f7ff;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        border: 2px solid #1890ff;
    }
    .main-header {
        color: #1a237e;
        text-align: center;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# --- Initial Page Load & State Management ---
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = generate_warehouse_data()
    st.session_state.df_analyzed = perform_abc_analysis(st.session_state.df_raw)
    st.session_state.df_optimized = recommend_slotting(st.session_state.df_analyzed)
    st.session_state.kpis = calculate_kpis(st.session_state.df_raw, st.session_state.df_optimized)
    st.session_state.recommendations = {}
    st.session_state.summary = ""
    st.session_state.show_table = False

# --- Gemini API Configuration ---
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

# --- Main App Layout ---
st.markdown("<h1 class='main-header'>Smart Space Management</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>AI-Powered Warehouse Space Optimization</p>", unsafe_allow_html=True)
st.write("") # Spacer

# Top section with refresh button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Refresh Data"):
        st.session_state.df_raw = generate_warehouse_data()
        st.session_state.df_analyzed = perform_abc_analysis(st.session_state.df_raw)
        st.session_state.df_optimized = recommend_slotting(st.session_state.df_analyzed)
        st.session_state.kpis = calculate_kpis(st.session_state.df_raw, st.session_state.df_optimized)
        st.session_state.summary = ""
        st.session_state.show_table = False
        st.rerun()

# --- KPI Dashboard Section ---
st.subheader("Key Performance Indicators at a Glance")
kpi_cols = st.columns(3)
with kpi_cols[0]:
    st.metric("Storage Utilization Rate", st.session_state.kpis['Storage_Utilization_Rate_Pct'])
with kpi_cols[1]:
    st.metric("Average Pick Time", st.session_state.kpis['Average_Pick_Time_Sec'] + "s")
with kpi_cols[2]:
    st.metric("Inventory Consolidation Index", st.session_state.kpis['Inventory_Consolidation_Index'])

kpi_cols2 = st.columns(3)
with kpi_cols2[0]:
    st.metric("Slotting Accuracy", st.session_state.kpis['Slotting_Accuracy_Pct'])
with kpi_cols2[1]:
    st.metric("ABC Zone Efficiency", st.session_state.kpis['ABC_Zone_Efficiency_Pct'])
with kpi_cols2[2]:
    st.metric("Space Cost per Unit", st.session_state.kpis['Space_Cost_Per_Unit'])

st.write("---")

# --- Agent Contribution Section ---
st.subheader("AI Agent Workflow")
st.write("The following AI agents work together in a sequence to provide comprehensive optimization insights.")
agent_cols = st.columns(11)
with agent_cols[0]:
    st.markdown("<div class='agent-box'>🗄️ Data Agent</div>", unsafe_allow_html=True)
with agent_cols[1]:
    st.markdown("<div style='text-align: center;'>➡️</div>", unsafe_allow_html=True)
with agent_cols[2]:
    st.markdown("<div class='agent-box'>📈 Inventory Agent</div>", unsafe_allow_html=True)
with agent_cols[3]:
    st.markdown("<div style='text-align: center;'>➡️</div>", unsafe_allow_html=True)
with agent_cols[4]:
    st.markdown("<div class='agent-box'>📍 Slotting Agent</div>", unsafe_allow_html=True)
with agent_cols[5]:
    st.markdown("<div style='text-align: center;'>➡️</div>", unsafe_allow_html=True)
with agent_cols[6]:
    st.markdown("<div class='agent-box'>📊 KPI Agent</div>", unsafe_allow_html=True)
with agent_cols[7]:
    st.markdown("<div style='text-align: center;'>➡️</div>", unsafe_allow_html=True)
with agent_cols[8]:
    st.markdown("<div class='agent-box'>🧠 Recommendation Agent</div>", unsafe_allow_html=True)
with agent_cols[9]:
    st.markdown("<div style='text-align: center;'>➡️</div>", unsafe_allow_html=True)
with agent_cols[10]:
    st.markdown("<div class='agent-box'>✍️ Gemini Model</div>", unsafe_allow_html=True)
st.write("") # Spacer

# --- Visualization Section ---
st.subheader("Visual Analysis of Inventory")
abc_df = pd.DataFrame(st.session_state.kpis['abc_distribution'].items(), columns=['Category', 'Count'])
fig = px.pie(abc_df, values='Count', names='Category', title='ABC Inventory Distribution', color_discrete_sequence=px.colors.qualitative.Pastel)

# *** THIS IS THE FIX ***
st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

# --- Run Optimization Button (at the bottom) ---
st.markdown("---")
st.write("Click the button below to perform a full optimization analysis and get a detailed executive summary.")
if st.button("Run Optimization"):
    with st.spinner("Analyzing and optimizing..."):
        st.session_state.df_raw = generate_warehouse_data()
        st.session_state.df_analyzed = perform_abc_analysis(st.session_state.df_raw)
        st.session_state.df_optimized = recommend_slotting(st.session_state.df_analyzed)
        st.session_state.kpis = calculate_kpis(st.session_state.df_raw, st.session_state.df_optimized)
        st.session_state.recommendations = generate_kpi_recommendations(st.session_state.kpis)
        st.session_state.summary = generate_summary_with_gemini(st.session_state.kpis, st.session_state.recommendations)
        st.session_state.show_table = True
    st.success("Optimization analysis complete!")
    st.rerun()


# --- Dynamic Recommendation Section (appears after clicking the button) ---
if st.session_state.show_table:
    st.subheader("Detailed Recommendations")
    rec_cols = st.columns(2)
    recs = list(st.session_state.recommendations.values())
    
    with rec_cols[0]:
        st.info(recs[0])
        st.info(recs[2])
        st.info(recs[4])

    with rec_cols[1]:
        st.info(recs[1])
        st.info(recs[3])
        st.info(recs[5])
        
    st.write("---")

    # The table is now here
    st.subheader("Optimized Warehouse Layout Recommendations")
    st.write("This table shows the recommended new locations for each product based on the ABC analysis.")
    st.dataframe(st.session_state.df_optimized[['Product_ID', 'ABC_Category', 'Daily_Demand', 'Current_Location', 'New_Location']])

    st.write("---")

    st.subheader("AI-Powered Executive Summary")
    st.info(st.session_state.summary)

    # Download button
    summary_text = st.session_state.summary
    st.download_button(
        label="Download Executive Summary",
        data=summary_text,
        file_name="AI_Powered_Summary.txt",
        mime="text/plain"
    )
