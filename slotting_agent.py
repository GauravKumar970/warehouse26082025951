import pandas as pd

def recommend_slotting(df_analyzed):
    df_optimized = df_analyzed.copy()
    
    # Sort by category (A, B, C) and then by daily demand
    df_optimized['ABC_Category_Sort'] = df_optimized['ABC_Category'].map({'A': 1, 'B': 2, 'C': 3})
    df_optimized = df_optimized.sort_values(by=['ABC_Category_Sort', 'Daily_Demand'], ascending=[True, False])
    
    # Assign new optimized locations (e.g., LOC_A01, LOC_B01, etc.)
    df_optimized['New_Location'] = 'TBD'
    
    # Simple example of assigning new locations based on category
    a_count = 1
    b_count = 1
    c_count = 1
    
    for index, row in df_optimized.iterrows():
        if row['ABC_Category'] == 'A':
            df_optimized.loc[index, 'New_Location'] = f"LOC_A{a_count:02}"
            a_count += 1
        elif row['ABC_Category'] == 'B':
            df_optimized.loc[index, 'New_Location'] = f"LOC_B{b_count:02}"
            b_count += 1
        else: # C
            df_optimized.loc[index, 'New_Location'] = f"LOC_C{c_count:02}"
            c_count += 1
            
    df_optimized = df_optimized.drop(columns=['ABC_Category_Sort'])
    return df_optimized

if __name__ == '__main__':
    from data_simulator import generate_warehouse_data
    from inventory_agent import perform_abc_analysis
    
    df_raw = generate_warehouse_data()
    df_analyzed = perform_abc_analysis(df_raw)
    df_optimized = recommend_slotting(df_analyzed)
    
    print(df_optimized[['Product_ID', 'ABC_Category', 'New_Location']].head(10))
