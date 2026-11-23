import pandas as pd

from app.tools.python_analyzer import (
    get_dataframe_summary,
    calculate_percentage_change,
    group_and_aggregate,
)

# Sample business dataset
data = {
    "category": ["Electronics", "Electronics", "Clothing", "Clothing", "Furniture"],
    "revenue": [50000, 70000, 30000, 40000, 60000],
    "orders": [100, 120, 80, 90, 110],
}

df = pd.DataFrame(data)


# Test 1: Dataset summary
print("\n--- DATAFRAME SUMMARY ---")

summary = get_dataframe_summary(df)

print(summary)


# Test 2: Percentage change
print("\n--- PERCENTAGE CHANGE ---")

growth = calculate_percentage_change(
    current_value=414479117.54, previous_value=290033761.06
)

print("Revenue Growth:", growth, "%")


# Test 3: Group and aggregate
print("\n--- REVENUE BY CATEGORY ---")

result = group_and_aggregate(
    df=df, group_by="category", metric="revenue", aggregation="sum"
)

print(result)
