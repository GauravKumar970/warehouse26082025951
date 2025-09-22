import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

# Import AI agents
from data_agent import generate_warehouse_data
from inventory_agent import perform_abc_analysis
from slotting_agent import recommend_slotting
from kpi_agent import calculate_kpis
from recommendation_agent import generate_kpi_recommendations

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Smart Space Management")

# --- Custom CSS for Aesthetics ---
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        color: #004d40;
        text-align: center;
        font-weight: bold;
        font-size: 2.5em;
        margin-top: -20px;
    }
    .subheader {
        color: #263238;
        font-size: 1.5em;
        font-weight: bold;
        margin-top: 20px;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 5px;
    }
    .section-separator {
        margin: 40px 0;
        border-top: 2px solid #cfd8dc;
    }
    /* KPI card styling */
    .stMetric {
        background-color: #f5f5f5;
        border-left: 5px solid #009688;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    /* Button styling */
    .stButton>button {
        background-color: #00796b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 12px 24px;
        width: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #004d40;
    }
    /* Agent flow boxes */
    .agent-box {
        background-color: #e0f2f1;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        border: 1px solid #009688;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    /* Custom container for data tables */
    .data-container {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
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
    st.session_state.show_results = False

# --- Gemini API Configuration ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_summary_with_gemini(kpis):
    prompt = f"""
    You are a data-driven AI assistant. Based on the following KPI data from a warehouse optimization run, provide a concise, bullet-point executive summary. Focus on actionable insights and key metrics.

    Here are the KPI results:
    - Storage Utilization Rate: {kpis.get('Storage_Utilization_Rate_Pct', 'N/A')}
    - Inventory Consolidation Index: {kpis.get('Inventory_Consolidation_Index', 'N/A')}
    - Average Pick Time: {kpis.get('Average_Pick_Time_Sec', 'N/A')}s
    - Total SKUs: {kpis.get('Total_SKUs', 'N/A')}

    **Instructions:**
    1.  Start with a clear, one-sentence conclusion.
    2.  Provide 3-4 bullet points highlighting the most impactful actions and metrics.
    3.  Focus on numbers and specific outcomes rather than general statements.
    4.  End with a call to action.
    """
    response = model.generate_content(prompt)
    return response.text

# --- Main App Layout ---
st.markdown("<h1 class='main-header'>Smart Space Management</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>AI-Powered Warehouse Space Optimization</p>", unsafe_allow_html=True)
st.write("")

# Top section with refresh button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Refresh Data"):
        st.session_state.df_raw = generate_warehouse_data()
        st.session_state.df_analyzed = perform_abc_analysis(st.session_state.df_raw)
        st.session_state.df_optimized = recommend_slotting(st.session_state.df_analyzed)
        st.session_state.kpis = calculate_kpis(st.session_state.df_raw, st.session_state.df_optimized)
        st.session_state.summary = ""
        st.session_state.show_results = False
        st.rerun()

# --- KPI Dashboard Section ---
st.markdown("<h2 class='subheader'>Key Performance Indicators at a Glance</h2>", unsafe_allow_html=True)
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

st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

# --- Agent Contribution Section ---
st.markdown("<h2 class='subheader'>AI Agent Workflow</h2>", unsafe_allow_html=True)
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
st.write("")

# --- Visualization Section ---
st.markdown("<h2 class='subheader'>Visual Analysis of Inventory</h2>", unsafe_allow_html=True)
abc_df = pd.DataFrame(st.session_state.kpis['abc_distribution'].items(), columns=['Category', 'Count'])
fig = px.pie(abc_df, values='Count', names='Category', title='ABC Inventory Distribution', color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

# --- Run Optimization Button ---
st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
st.write("Click the button below to perform a full optimization analysis and get a detailed executive summary.")
if st.button("Run Optimization"):
    with st.spinner("Analyzing and optimizing..."):
        st.session_state.df_raw = generate_warehouse_data()
        st.session_state.df_analyzed = perform_abc_analysis(st.session_state.df_raw)
        st.session_state.df_optimized = recommend_slotting(st.session_state.df_analyzed)
        st.session_state.kpis = calculate_kpis(st.session_state.df_raw, st.session_state.df_optimized)
        st.session_state.recommendations = generate_kpi_recommendations(st.session_state.kpis)
        st.session_state.summary = generate_summary_with_gemini(st.session_state.kpis)
        st.session_state.show_results = True
    st.success("Optimization analysis complete!")
    st.rerun()

# --- Dynamic Results Section (appears after clicking the button) ---
if st.session_state.show_results:
    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # 1. Detailed Recommendations (Table)
    st.markdown("<h2 class='subheader'>Detailed Recommendations & Action Plan</h2>", unsafe_allow_html=True)
    st.markdown("<div class='data-container'>", unsafe_allow_html=True)
    st.dataframe(st.session_state.recommendations.set_index('KPI'), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # 2. Optimized Warehouse Layout (Table)
    st.markdown("<h2 class='subheader'>Optimized Warehouse Layout Recommendations</h2>", unsafe_allow_html=True)
    st.write("This table shows the precise relocation plan for each product.")
    st.markdown("<div class='data-container'>", unsafe_allow_html=True)
    st.dataframe(st.session_state.df_optimized[['Product_ID', 'ABC_Category', 'Daily_Demand', 'Current_Location', 'New_Location']], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # 3. AI-Powered Executive Summary (Text & Graph)
    st.markdown("<h2 class='subheader'>AI-Powered Executive Summary</h2>", unsafe_allow_html=True)
    summary_cols = st.columns([2,1])
    with summary_cols[0]:
        st.markdown(st.session_state.summary)

    with summary_cols[1]:
        kpi_summary_data = {
            'Metric': ['Storage Utilization Rate', 'Average Pick Time'],
            'Value': [
                float(st.session_state.kpis['Storage_Utilization_Rate_Pct'].replace('%', '')),
                float(st.session_state.kpis['Average_Pick_Time_Sec'])
            ]
        }
        kpi_summary_df = pd.DataFrame(kpi_summary_data)
        fig_summary = px.bar(kpi_summary_df, x='Metric', y='Value', color='Metric', title='Key Performance Metrics')
        st.plotly_chart(fig_summary, use_container_width=True)
    
    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # Download button
    summary_text = st.session_state.summary
    st.download_button(
        label="Download Executive Summary",
        data=summary_text,
        file_name="AI_Powered_Summary.txt",
        mime="text/plain"
    )
