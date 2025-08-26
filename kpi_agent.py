def calculate_kpis(df_before, df_after):
    total_volume_before = df_before['current_stock'].sum()
    total_volume_after = df_after['current_stock'].sum()
    storage_utilization_rate = (total_volume_after / total_volume_before) * 100
    consolidation_index = 100  # Placeholder
    avg_pick_time = 30  # Placeholder
    slotting_accuracy = 90  # Placeholder
    abc_efficiency = 85  # Placeholder
    space_cost_per_unit = 500000 / total_volume_after
    return {
        'Storage Utilization Rate (%)': round(storage_utilization_rate, 2),
        'Inventory Consolidation Index': consolidation_index,
        'Average Pick Time (seconds/order)': avg_pick_time,
        'Slotting Accuracy (%)': slotting_accuracy,
        'ABC Zone Efficiency (%)': abc_efficiency,
        'Space Cost per Unit Stored': round(space_cost_per_unit, 2)
    }
