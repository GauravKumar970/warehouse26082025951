import pandas as pd

def recommend_slotting(df):
    df['recommended_location'] = df['location_id']
    df.loc[df['abc_category'] == 'A', 'recommended_location'] = 'A-ZONE'
    df.loc[df['abc_category'] == 'B', 'recommended_location'] = 'B-ZONE'
    df.loc[df['abc_category'] == 'C', 'recommended_location'] = 'C-ZONE'
    return df
