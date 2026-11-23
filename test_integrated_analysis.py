from app.services.sql_generator import generate_sql
from app.tools.sql_executor import execute_sql

from app.tools.python_analyzer import get_dataframe_summary, group_and_aggregate

# 1. Ask a business question
question = """
Show total revenue by product category
for delivered orders in 2025.
"""

# 2. Generate SQL
sql = generate_sql(question)

print("\n--- GENERATED SQL ---")
print(sql)


# 3. Execute SQL
df = execute_sql(sql)

print("\n--- DATABASE RESULTS ---")
print(df)


# 4. Analyze the real database results
summary = get_dataframe_summary(df)

print("\n--- DATA SUMMARY ---")
print(summary)


# 5. Find the highest revenue category
result = group_and_aggregate(
    df=df, group_by="product_category", metric="total_revenue", aggregation="sum"
)

result = result.sort_values(by="total_revenue", ascending=False)

print("\n--- CATEGORY PERFORMANCE ---")
print(result)
