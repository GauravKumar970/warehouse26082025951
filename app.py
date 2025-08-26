import streamlit as st
import pandas as pd
from data_agent import generate_warehouse_data
from inventory_agent import perform_abc_analysis
from slotting_agent import recommend_slotting
from kpi_agent import calculate_kpis

st.title("Smart Space Management: AI-Driven Warehouse Optimization")

if st.button("Run Optimization"):
    # Create a simple progress bar
    progress_bar = st.progress(0)

    # Step 1: Generate Raw Data
    with st.spinner('Generating raw warehouse data...'):
        df_raw = generate_warehouse_data()
    progress_bar.progress(25)

    # Step 2: Perform ABC Analysis
    with st.spinner('Performing ABC analysis on inventory...'):
        df_analyzed = perform_abc_analysis(df_raw)
    progress_bar.progress(50)

    # Step 3: Recommend Slotting
    with st.spinner('Recommending optimized slotting locations...'):
        df_optimized = recommend_slotting(df_analyzed)
    progress_bar.progress(75)

    # Step 4: Calculate KPIs
    with st.spinner('Calculating key performance indicators...'):
        kpis = calculate_kpis(df_raw, df_optimized)
    progress_bar.progress(100)
    st.success('Optimization complete!')

    st.subheader("Key Performance Indicators")
    for k, v in kpis.items():
        st.write(f"**{k}**: {v}")

    st.subheader("Optimized Warehouse Layout Recommendations")
    st.write(df_optimized[['Product_ID', 'ABC_Category', 'Daily_Demand', 'Current_Location', 'New_Location']])
