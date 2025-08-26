import pandas as pd

def calculate_kpis(df_raw, df_optimized):
    kpis = {}
    
    # 1. Total SKUs and ABC Category Distribution
    kpis['Total_SKUs'] = df_raw.shape[0]
    category_counts = df_optimized['ABC_Category'].value_counts()
    
    # Returning raw numbers for visualization
    abc_distribution = category_counts.to_dict()
    kpis['abc_distribution'] = abc_distribution
    
    for cat in category_counts.index:
        kpis[f"Products_in_Category_{cat}"] = int(category_counts[cat])
        
    kpis['Percentage_A_Products'] = f"{kpis['Products_in_Category_A'] / kpis['Total_SKUs'] * 100:.2f}%"
    kpis['Percentage_B_Products'] = f"{kpis['Products_in_Category_B'] / kpis['Total_SKUs'] * 100:.2f}%"
    kpis['Percentage_C_Products'] = f"{kpis['Products_in_Category_C'] / kpis['Total_SKUs'] * 100:.2f}%"

    # 2. Storage Utilization Rate (%) (Simulated)
    total_slots = 150
    occupied_slots = df_optimized.shape[0]
    kpis['Storage_Utilization_Rate_Pct'] = f"{(occupied_slots / total_slots) * 100:.2f}%"

    # 3. Inventory Consolidation Index (Simulated)
    initial_locations = df_raw['Current_Location'].nunique()
    optimized_locations = df_optimized['New_Location'].nunique()
    kpis['Initial_Locations'] = initial_locations
    kpis['Optimized_Locations'] = optimized_locations
    kpis['Inventory_Consolidation_Index'] = f"{((initial_locations - optimized_locations) / initial_locations) * 100:.2f}%"

    # 4. Average Pick Time (seconds/order) (Simulated)
    pick_time_A = 20  # seconds
    pick_time_B = 60  # seconds
    pick_time_C = 120 # seconds
    
    total_pick_time = (
        (df_optimized[df_optimized['ABC_Category'] == 'A']['Daily_Demand'].sum() * pick_time_A) +
        (df_optimized[df_optimized['ABC_Category'] == 'B']['Daily_Demand'].sum() * pick_time_B) +
        (df_optimized[df_optimized['ABC_Category'] == 'C']['Daily_Demand'].sum() * pick_time_C)
    )
    total_demand = df_optimized['Daily_Demand'].sum()
    kpis['Average_Pick_Time_Sec'] = f"{(total_pick_time / total_demand):.2f}"

    # 5. Slotting Accuracy (%) (Simulated)
    kpis['Slotting_Accuracy_Pct'] = "100.00%"
    
    # 6. ABC Zone Efficiency (%) (Simulated)
    kpis['ABC_Zone_Efficiency_Pct'] = "95.00%"

    # 7. Space Cost per Unit Stored (Simulated)
    total_space_cost = 50000
    total_units = df_optimized.shape[0]
    kpis['Space_Cost_Per_Unit'] = f"${(total_space_cost / total_units):.2f}"

    return kpis

if __name__ == '__main__':
    from data_agent import generate_warehouse_data
    from inventory_agent import perform_abc_analysis
    from slotting_agent import recommend_slotting
    
    df_raw = generate_warehouse_data()
    df_analyzed = perform_abc_analysis(df_raw)
    df_optimized = recommend_slotting(df_analyzed)
    
    kpis = calculate_kpis(df_raw, df_optimized)
    for k, v in kpis.items():
        print(f"{k}: {v}")
