from app.services.sql_generator import generate_sql
from app.tools.sql_executor import execute_sql

question = """
Show the top 5 products by revenue
from delivered orders in 2025.
"""

# Generate SQL using Gemini
sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)

# Execute SQL using the read-only database user
df = execute_sql(sql)

print("\nQuery Results:")
print(df)

print("\nDataFrame Information:")
print(df.info())

try:
    df = execute_sql("SELECT * FROM orders")
    print("Rows returned:", len(df))

except Exception as error:
    print("Expected protection:", error)
