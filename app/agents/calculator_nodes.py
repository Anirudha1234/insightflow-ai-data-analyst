import pandas as pd

from app.tools.calculator import (
    calculate_profit,
    calculate_profit_margin,
    calculate_average_order_value,
    calculate_growth,
    calculate_percentage,
)


def calculator_node(state: dict) -> dict:
    try:
        question = state["question"].lower()
        df = state["dataframe"]
        # print("CALCULATOR QUESTION:", question)
        # print("CALCULATOR COLUMNS:", df.columns.tolist())

        calculations = {}

        # 1. Profit and profit margin
        if "profit" in question or "margin" in question:
            if df is None or df.empty:
                raise ValueError("No data available for profit calculation.")

            required_columns = {"revenue", "cost"}

            if not required_columns.issubset(df.columns):
                raise ValueError(
                    "Profit calculation requires revenue and cost columns. "
                    "The SQL query must provide both."
                )

            revenue = float(df["revenue"].sum())
            cost = float(df["cost"].sum())

            calculations["profit"] = calculate_profit(revenue, cost)
            calculations["profit_margin"] = calculate_profit_margin(revenue, cost)

        # 2. Average Order Value
        if "average order value" in question or "aov" in question:

            if df is None or df.empty:
                raise ValueError("No data available for AOV calculation.")

            # Recognize different SQL aliases for AOV
            aov_columns = [
                column
                for column in df.columns
                if "average" in column.lower()
                and "order" in column.lower()
                and "value" in column.lower()
            ]

            # Case 1: SQL has already calculated AOV
            if aov_columns:

                if len(aov_columns) != 1 or len(df) != 1:
                    raise ValueError("Expected exactly one AOV result from SQL.")

                aov = float(df[aov_columns[0]].iloc[0])

                calculations["average_order_value"] = round(aov, 2)

            # Case 2: Calculate AOV using revenue and order count
            elif {"revenue", "total_orders"}.issubset(df.columns):

                revenue = float(df["revenue"].sum())
                total_orders = int(df["total_orders"].sum())

                calculations["average_order_value"] = calculate_average_order_value(
                    revenue, total_orders
                )

            else:
                raise ValueError(
                    "AOV calculation requires an average order value "
                    "column or revenue and total_orders columns."
                )

        # 3. Growth calculation
        if "growth" in question.lower():

            # Find an existing percentage-growth column
            growth_columns = [
                col
                for col in df.columns
                if "growth" in col.lower()
                and ("percentage" in col.lower() or "percent" in col.lower())
            ]

            if growth_columns and len(df) == 1:
                value = pd.to_numeric(df[growth_columns[0]].iloc[0], errors="coerce")

                if pd.notna(value):
                    calculations["revenue_growth"] = round(float(value), 2)

            # Otherwise calculate growth using current and previous revenue
            elif "current_revenue" in df.columns and "previous_revenue" in df.columns:
                current = float(df["current_revenue"].iloc[0])
                previous = float(df["previous_revenue"].iloc[0])

                calculations["revenue_growth"] = round(
                    calculate_growth(previous, current), 2
                )

            # Support year-based revenue columns
            elif "revenue_2024" in df.columns and "revenue_2025" in df.columns:
                previous = float(df["revenue_2024"].iloc[0])
                current = float(df["revenue_2025"].iloc[0])

                calculations["revenue_growth"] = round(
                    calculate_growth(previous, current), 2
                )

            else:
                raise ValueError(
                    "Growth calculation requires a percentage-growth "
                    "column or current and previous revenue columns."
                )

        # 4. Percentage contribution
        if "contribution" in question or "percentage" in question:

            if df is None or df.empty:
                raise ValueError("No data available for percentage calculation.")

            # Case 1: SQL has already calculated percentage
            percentage_columns = [
                column for column in df.columns if column.endswith("_percentage")
            ]

            if percentage_columns:

                if len(df) != 1:
                    raise ValueError("Expected one percentage result from SQL.")

                column = percentage_columns[0]
                value = df[column].iloc[0]

                if pd.isna(value):
                    raise ValueError("SQL returned an empty percentage result.")

                calculations["percentage"] = round(float(value), 2)

            # Case 2: Calculate percentage using part and total
            elif {"part", "total"}.issubset(df.columns):

                part = float(df["part"].sum())
                total = float(df["total"].sum())

                calculations["percentage"] = calculate_percentage(part, total)

            else:
                raise ValueError(
                    "Percentage calculation requires either a "
                    "percentage result column or part and total columns."
                )

            # print("CALCULATOR OUTPUT:", calculations)
        return {"calculations": calculations, "error": None, "status": "success"}

    except Exception as error:
        return {"calculations": {}, "error": str(error), "status": "error"}
