import pandas as pd

def generate_kpi_recommendations(kpis):
    # This will now return a structured list of dictionaries
    recommendations_data = [
        {
            "KPI": "Storage Utilization Rate",
            "Current State": kpis.get('Storage_Utilization_Rate_Pct', 'N/A'),
            "Action/Recommendation": "Optimize existing rack space and floor layout to accommodate new inventory efficiently.",
            "Additional Details": "Focus on high-density storage solutions for low-turnover items. Consider vertical storage options to maximize cubic space."
        },
        {
            "KPI": "Inventory Consolidation",
            "Current State": kpis.get('Inventory_Consolidation_Index', 'N/A'),
            "Action/Recommendation": "Consolidate fragmented inventory by co-locating similar SKUs.",
            "Additional Details": "Move all products from 'Current Location' to the recommended 'New Location' to improve pick-path efficiency and reduce space wastage."
        },
        {
            "KPI": "Average Pick Time",
            "Current State": kpis.get('Average_Pick_Time_Sec', 'N/A') + "s",
            "Action/Recommendation": "Reduce picker travel distance by placing high-demand 'A' category items in the most accessible zones.",
            "Additional Details": "Ensure the fastest moving SKUs are closest to the shipping docks. Consider a separate zone for order picking."
        },
        {
            "KPI": "ABC Zone Efficiency",
            "Current State": kpis.get('ABC_Zone_Efficiency_Pct', 'N/A'),
            "Action/Recommendation": "Maintain the optimal layout based on demand to improve workflow.",
            "Additional Details": "Implement a continuous review process to re-evaluate product classifications quarterly and update the layout as demand patterns change."
        },
        {
            "KPI": "Space Cost per Unit",
            "Current State": kpis.get('Space_Cost_Per_Unit', 'N/A'),
            "Action/Recommendation": "Identify and remove low-performing, low-demand SKUs to reduce long-term storage costs.",
            "Additional Details": "Flag products that have not been picked in the last 90 days. Collaborate with the sales team to either promote or phase out these items."
        },
        {
            "KPI": "Detailed Recommendations",
            "Current State": f"{kpis.get('Total_SKUs', 'N/A')} SKUs",
            "Action/Recommendation": "Utilize the 'Optimized Warehouse Layout' table for a precise SKU-by-SKU relocation plan.",
            "Additional Details": "The attached table provides the exact 'New Location' for each product, enabling immediate action on the warehouse floor."
        }
    ]
    return pd.DataFrame(recommendations_data)
