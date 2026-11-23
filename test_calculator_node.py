import pandas as pd

from app.agents.calculator_nodes import calculator_node

# Test 1: Profit and Profit Margin
profit_state = {
    "question": "Calculate profit and profit margin",
    "dataframe": pd.DataFrame({"revenue": [100000, 50000], "cost": [70000, 30000]}),
}

# Test 2: Average Order Value
aov_state = {
    "question": "Calculate average order value",
    "dataframe": pd.DataFrame({"revenue": [100000, 50000], "total_orders": [20, 10]}),
}

# Test 3: Revenue Growth
growth_state = {
    "question": "Calculate revenue growth",
    "dataframe": pd.DataFrame(
        {"current_revenue": [150000], "previous_revenue": [100000]}
    ),
}

# Test 4: Percentage Contribution
percentage_state = {
    "question": "Calculate percentage contribution",
    "dataframe": pd.DataFrame({"part": [30000], "total": [100000]}),
}

# Test 5: Missing required columns
error_state = {
    "question": "Calculate profit and profit margin",
    "dataframe": pd.DataFrame({"total_revenue": [100000]}),
}


tests = [
    ("Profit Test", profit_state),
    ("AOV Test", aov_state),
    ("Growth Test", growth_state),
    ("Percentage Test", percentage_state),
    ("Error Handling Test", error_state),
]

for test_name, state in tests:
    print(f"\n--- {test_name} ---")

    result = calculator_node(state)

    print("Status:", result["status"])
    print("Calculations:", result.get("calculations"))

    if result.get("error"):
        print("Error:", result["error"])
