import pandas as pd
import numpy as np

def generate_warehouse_data(num_skus=1000):
    data = {
        'sku_id': [f'SKU-{i:04d}' for i in range(num_skus)],
        'current_stock': np.random.randint(10, 500, num_skus),
        'monthly_sales': np.random.randint(1, 250, num_skus),
        'unit_cost': np.random.uniform(5.0, 500.0, num_skus),
        'location_id': [f'LOC-{i:03d}' for i in range(num_skus)],
    }
    return pd.DataFrame(data)
