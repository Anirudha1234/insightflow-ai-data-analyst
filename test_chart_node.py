import pandas as pd

from app.agents.chart_nodes import generate_chart_node

df = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Books", "Sports"],
        "revenue": [100000, 50000, 25000, 40000],
    }
)


questions = [
    "Show revenue by category with a bar chart",
    "Plot monthly revenue as a line chart",
    "Show revenue contribution as a pie chart",
    "Show a scatter plot of revenue",
]


for question in questions:

    result = generate_chart_node({"question": question, "dataframe": df})

    print("\nQuestion:", question)
    print("Chart type:", result.get("chart_type"))
    print("Chart path:", result.get("chart_path"))
    print("Status:", result["status"])
    print("Error:", result.get("error"))
