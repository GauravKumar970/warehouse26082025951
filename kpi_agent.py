import pandas as pd

def calculate_kpis(df_raw, df_optimized):
    kpis = {}
    
    # Total number of SKUs
    kpis['Total_SKUs'] = df_raw.shape[0]
    
    # Products by category
    category_counts = df_optimized['ABC_Category'].value_counts()
    for cat in category_counts.index:
        kpis[f"Products_in_Category_{cat}"] = int(category_counts[cat])

    # Percentage of products by category
    kpis['Percentage_A_Products'] = f"{kpis['Products_in_Category_A'] / kpis['Total_SKUs'] * 100:.2f}%"
    kpis['Percentage_B_Products'] = f"{kpis['Products_in_Category_B'] / kpis['Total_SKUs'] * 100:.2f}%"
    kpis['Percentage_C_Products'] = f"{kpis['Products_in_Category_C'] / kpis['Total_SKUs'] * 100:.2f}%"
    
    # A simple KPI: Improvement in picking efficiency (hypothetical)
    # We assume 'A' items are now in the most accessible locations
    # Old model: random locations, so picking path is long
    # New model: 'A' items are grouped, reducing path length
    
    # Hypothetical old efficiency score (random locations)
    old_efficiency = 100
    
    # New efficiency is better because 'A' items are clustered
    # The bonus is proportional to the number of 'A' items
    new_efficiency = old_efficiency * (1 + (kpis['Products_in_Category_A'] / kpis['Total_SKUs'] * 0.5))
    kpis['Picking_Efficiency_Improvement'] = f"{new_efficiency / old_efficiency * 100 - 100:.2f}%"
    
    return kpis

if __name__ == '__main__':
    from data_simulator import generate_warehouse_data
    from inventory_agent import perform_abc_analysis
    from slotting_agent import recommend_slotting
    
    df_raw = generate_warehouse_data()
    df_analyzed = perform_abc_analysis(df_raw)
    df_optimized = recommend_slotting(df_analyzed)
    
    kpis = calculate_kpis(df_raw, df_optimized)
    for k, v in kpis.items():
        print(f"{k}: {v}")
