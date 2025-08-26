def generate_kpi_recommendations(kpis):
    recommendations = {}

    recommendations['Storage_Utilization_Rate_Pct'] = (
        "**Recommendation for Storage Utilization:** The current utilization is at {}. "
        "To improve, consider re-evaluating the long-tail assortment to free up valuable space."
    ).format(kpis['Storage_Utilization_Rate_Pct'])

    recommendations['Inventory_Consolidation_Index'] = (
        "**Recommendation for Inventory Consolidation:** The optimization process consolidated {} initial locations to {} new locations. "
        "This resulted in a {} consolidation index, significantly reducing fragmented storage and improving efficiency."
    ).format(kpis['Initial_Locations'], kpis['Optimized_Locations'], kpis['Inventory_Consolidation_Index'])

    recommendations['Average_Pick_Time_Sec'] = (
        "**Recommendation for Pick Time:** The current average pick time is approximately {} seconds. "
        "This is a direct result of placing high-demand 'A' items in easily accessible locations, "
        "which minimizes travel time for pickers."
    ).format(kpis['Average_Pick_Time_Sec'])

    recommendations['Slotting_Accuracy_Pct'] = (
        "**Recommendation for Slotting Accuracy:** The current slotting accuracy is {}. "
        "This indicates a high degree of precision in item placement. To maintain this, "
        "ensure a regular review of inventory profiles and update the slotting strategy accordingly."
    ).format(kpis['Slotting_Accuracy_Pct'])

    recommendations['ABC_Zone_Efficiency_Pct'] = (
        "**Recommendation for ABC Zone Efficiency:** The 'A' zone efficiency is currently at {}. "
        "This high utilization demonstrates that prime space is effectively allocated to fast-moving inventory. "
        "Continue to monitor demand patterns to prevent overstocking."
    ).format(kpis['ABC_Zone_Efficiency_Pct'])

    recommendations['Space_Cost_Per_Unit'] = (
        "**Recommendation for Space Cost:** With an average space cost of {} per unit, the current strategy is cost-efficient. "
        "Further reductions can be achieved by eliminating slow-moving SKUs."
    ).format(kpis['Space_Cost_Per_Unit'])

    return recommendations
