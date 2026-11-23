import pandas as pd

from app.agents.analysis_nodes import python_analysis_node

# Sample data similar to our actual SQL query results
df = pd.DataFrame(
    {
        "product_id": [1, 2, 3, 4, 5],
        "product_name": [
            "Product A",
            "Product B",
            "Product C",
            "Product D",
            "Product E",
        ],
        "average_selling_price": [100, 200, 300, 400, 500],
        "total_revenue": [1000, 2500, 3500, 5000, 6500],
    }
)


# Prepare LangGraph state
state = {
    "question": "Analyze the relationship between selling price and revenue",
    "dataframe": df,
}


# Execute node
result = python_analysis_node(state)


print("\n--- PYTHON ANALYSIS RESULTS ---")
print(result)

print("\n--- CORRELATION ---")
print(result["python_analysis"].get("correlation"))

print("\n--- STATUS ---")
print(result["status"])
