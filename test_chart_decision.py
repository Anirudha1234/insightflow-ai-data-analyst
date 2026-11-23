from app.agents.chart_nodes import check_chart_requirement_node

questions = [
    "Show top 5 products by revenue",
    "Plot monthly revenue for 2025",
    "Visualize revenue by category",
    "Show a pie chart of sales contribution",
    "Compare monthly sales using a graph",
]


for question in questions:

    result = check_chart_requirement_node({"question": question})

    print("\nQuestion:", question)
    print("Chart required:", result["chart_required"])
