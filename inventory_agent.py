import pandas as pd

def perform_abc_analysis(df):
    df['total_value'] = df['monthly_sales'] * 12 * df['unit_cost']
    df_sorted = df.sort_values(by='total_value', ascending=False).reset_index(drop=True)
    df_sorted['cumulative_value'] = df_sorted['total_value'].cumsum()
    df_sorted['cumulative_percentage'] = (df_sorted['cumulative_value'] / df_sorted['total_value'].sum()) * 100
    df_sorted['abc_category'] = 'C'
    df_sorted.loc[df_sorted['cumulative_percentage'] <= 80, 'abc_category'] = 'B'
    df_sorted.loc[df_sorted['cumulative_percentage'] <= 20, 'abc_category'] = 'A'
    return df_sorted
