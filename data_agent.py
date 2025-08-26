import numpy as np
import pandas as pd

def generate_warehouse_data():
    # np.random.seed(42)  <-- This line has been removed
    data = {
        'Product_ID': [f'PROD_{i+1:03}' for i in range(100)],
        'Item_Type': np.random.choice(['SKU', 'Non-SKU'], 100, p=[0.8, 0.2]),
        'Product_Category': np.random.choice(['Electronics', 'Apparel', 'Home Goods', 'Beauty', 'Groceries'], 100),
        'Daily_Demand': np.random.randint(1, 101, 100),
        'Dimensions_cm': [f"{np.random.randint(10, 50)}x{np.random.randint(10, 50)}x{np.random.randint(10, 50)}" for _ in range(100)],
        'Weight_kg': np.random.uniform(0.1, 50, 100).round(2),
        'Current_Location': np.random.choice([f'LOC_{i+1:02}' for i in range(50)], 100)
    }
    return pd.DataFrame(data)

if __name__ == '__main__':
    df = generate_warehouse_data()
    print(df.head())
    print("\nDataFrame Info:")
    df.info()
