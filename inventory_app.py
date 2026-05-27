%%writefile inventory_app.py
import streamlit as st
import statistics
import math
from scipy.stats import norm

def main():
    st.title("📦 Inventory Management Calculator")
    st.write("This app calculates EOQ, Safety Stock, and Reorder Point based on your inputs.")

    # EOQ Inputs
    st.header("Step 1: Economic Order Quantity (EOQ)")
    annual_demand = st.number_input("Annual Demand", min_value=1, value=1000)
    holding_cost = st.number_input("Holding Cost (per item per year)", min_value=1, value=5)
    order_cost = st.number_input("Order Cost (per order)", min_value=1, value=50)
    lead_time = st.number_input("Lead Time (in weeks)", min_value=1, value=2)

    eoq = math.sqrt((2 * annual_demand * order_cost) / holding_cost)
    eoq = int(eoq)
    st.success(f"Economic Order Quantity (EOQ): {eoq}")

    # Demand stats
    st.header("Step 2: Demand Statistics")
    demand_input = st.text_input("Enter daily demand values separated by spaces", "100 120 110 130 115")
    if demand_input:
        demand = [int(x) for x in demand_input.split()]
        average = statistics.mean(demand)
        std_dev = statistics.stdev(demand)
        st.write(f"Average Daily Demand: {average}")
        st.write(f"Standard Deviation of Demand: {std_dev}")

        # Safety Stock
        st.header("Step 3: Safety Stock")
        service_level = st.slider("Service Level", min_value=0.95, max_value=0.99, value=0.97)
        mean_demand_over_lead_time = int(average * lead_time * 7)
        std_dev_demand_over_lead_time = std_dev * math.sqrt(lead_time * 7)
        z_score = norm.ppf(service_level)
        safety_stock = int(z_score * std_dev_demand_over_lead_time)

        st.write(f"Mean Demand Over Lead Time: {mean_demand_over_lead_time}")
        st.write(f"Standard Deviation Over Lead Time: {std_dev_demand_over_lead_time:.2f}")
        st.success(f"Safety Stock: {safety_stock}")

        # Reorder Point
        st.header("Step 4: Reorder Point")
        reorder_point = int(((annual_demand / 52) * lead_time) + safety_stock)
        st.success(f"Reorder Point: {reorder_point}")
        st.info(f"➡ Place an order of {eoq} units whenever inventory reaches {reorder_point} units.")

if __name__ == "__main__":
    main()
