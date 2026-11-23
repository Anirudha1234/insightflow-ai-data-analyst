import pandas as pd

from app.tools.chart_generator import (
    generate_bar_chart,
    generate_line_chart,
    generate_pie_chart,
    generate_scatter_chart,
)

# Sample business data
df = pd.DataFrame(
    {
        "category": ["Electronics", "Home & Kitchen", "Sports", "Clothing", "Books"],
        "revenue": [291498157.06, 57633549.25, 45435311.70, 15920796.73, 3991302.80],
        "orders": [500, 300, 250, 150, 80],
    }
)


# 1. Bar Chart
bar_fig = generate_bar_chart(
    df, x="category", y="revenue", title="Revenue by Product Category"
)

bar_fig.write_html("data/revenue_bar_chart.html")


# 2. Pie Chart
pie_fig = generate_pie_chart(
    df, names="category", values="revenue", title="Revenue Contribution by Category"
)

pie_fig.write_html("data/revenue_pie_chart.html")


# 3. Scatter Chart
scatter_fig = generate_scatter_chart(
    df, x="orders", y="revenue", title="Orders vs Revenue"
)

scatter_fig.write_html("data/orders_revenue_scatter.html")


# 4. Line Chart
monthly_df = pd.DataFrame(
    {
        "month": [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        "revenue": [20, 25, 22, 30, 35, 32, 40, 45, 42, 50, 55, 60],
    }
)

line_fig = generate_line_chart(
    monthly_df, x="month", y="revenue", title="Monthly Revenue Trend"
)

line_fig.write_html("data/monthly_revenue_chart.html")


print("All four charts generated successfully!")
