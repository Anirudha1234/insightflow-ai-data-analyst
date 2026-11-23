import os
import pandas as pd

from app.tools.chart_generator import (
    generate_bar_chart,
    generate_line_chart,
    generate_pie_chart,
    generate_scatter_chart,
)


def check_chart_requirement_node(state: dict) -> dict:

    question = state["question"].lower()

    chart_keywords = [
        "chart",
        "plot",
        "visualize",
        "visualise",
        "graph",
        "visualization",
        "visualisation",
    ]

    chart_required = any(keyword in question for keyword in chart_keywords)

    return {"chart_required": chart_required, "status": "success"}


def generate_chart_node(state: dict) -> dict:
    try:
        df = state["dataframe"].copy()
        question = state["question"].lower()

        os.makedirs("data", exist_ok=True)

        # Identify the requested chart type
        if "pie" in question:
            chart_type = "pie"
        elif "scatter" in question:
            chart_type = "scatter"
        elif "line" in question or "monthly" in question:
            chart_type = "line"
        else:
            chart_type = "bar"

        # Convert Decimal/object numeric columns into numeric dtype
        for column in df.columns:
            if df[column].dtype == "object":
                converted = pd.to_numeric(df[column], errors="coerce")

                if converted.notna().sum() == df[column].notna().sum():
                    df[column] = converted

        # Identify numeric and categorical columns
        numeric_columns = df.select_dtypes(include="number").columns.tolist()

        categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

        if chart_type == "scatter":

            # Exclude identifier columns from scatter-chart axes
            scatter_numeric_columns = [
                column
                for column in numeric_columns
                if column.lower() != "id" and not column.lower().endswith("_id")
            ]

            if len(scatter_numeric_columns) < 2:
                raise ValueError(
                    "Scatter charts require at least two "
                    "numeric columns other than identifiers."
                )

            x = scatter_numeric_columns[0]
            y = scatter_numeric_columns[1]

        else:
            if not numeric_columns:
                raise ValueError("No numeric column available for chart generation.")

            if not categorical_columns:
                raise ValueError("No categorical column available for the chart.")

            x = categorical_columns[0]
            y = numeric_columns[-1]

        title = state["question"]

        # Generate the chart
        if chart_type == "bar":
            fig = generate_bar_chart(df, x, y, title)

        elif chart_type == "line":
            fig = generate_line_chart(df, x, y, title)

        elif chart_type == "pie":
            fig = generate_pie_chart(df, x, y, title)

        elif chart_type == "scatter":
            fig = generate_scatter_chart(df, x, y, title)

        chart_path = os.path.join("data", f"insightflow_{chart_type}_chart.html")

        fig.write_html(chart_path)

        return {
            "chart_path": chart_path,
            "chart_type": chart_type,
            "status": "success",
            "error": None,
        }

    except Exception as error:
        return {"error": str(error), "status": "error"}
