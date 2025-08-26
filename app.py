
import streamlit as st
import pandas as pd
from data_agent import generate_warehouse_data
from inventory_agent import perform_abc_analysis
from slotting_agent import recommend_slotting
from kpi_agent import calculate_kpis

st.title("Smart Space Management: AI-Driven Warehouse Optimization")

if st.button("Run Optimization"):
    df_raw = generate_warehouse_data()
    df_analyzed = perform_abc_analysis(df_raw)
    df_optimized = recommend_slotting(df_analyzed)
    kpis = calculate_kpis(df_raw, df_optimized)

    st.subheader("Key Performance Indicators")
    for k, v in kpis.items():
        st.write(f"{k}: {v}")
