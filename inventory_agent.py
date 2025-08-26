import pandas as pd

def perform_abc_analysis(df):
    df_abc = df.copy()

    # Calculate total demand for each product
    df_abc['Total_Demand'] = df_abc['Daily_Demand']

    # Sort by total demand in descending order
    df_abc = df_abc.sort_values(by='Total_Demand', ascending=False)

    # Calculate cumulative percentage of demand
    df_abc['Cum_Demand'] = df_abc['Total_Demand'].cumsum()
    df_abc['Cum_Demand_Pct'] = 100 * df_abc['Cum_Demand'] / df_abc['Total_Demand'].sum()

    # Classify products into A, B, and C categories
    def classify_abc(row):
        if row['Cum_Demand_Pct'] <= 80:
            return 'A'
        elif row['Cum_Demand_Pct'] <= 95:
            return 'B'
        else:
            return 'C'

    df_abc['ABC_Category'] = df_abc.apply(classify_abc, axis=1)

    return df_abc

if __name__ == '__main__':
    from data_agent import generate_warehouse_data
    df = generate_warehouse_data()
    df_analyzed = perform_abc_analysis(df)
    print(df_analyzed[['Product_ID', 'Total_Demand', 'Cum_Demand_Pct', 'ABC_Category']].head())
    print("\nCategory distribution:")
    print(df_analyzed['ABC_Category'].value_counts())
