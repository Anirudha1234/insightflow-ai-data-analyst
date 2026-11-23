import pandas as pd
import numpy as np


def get_dataframe_summary(df: pd.DataFrame) -> dict:
    """
    Generate a general summary of a DataFrame.
    Automatically detects numeric values stored as objects.
    """

    if df.empty:
        return {"message": "No data available for analysis."}

    df = df.copy()

    # Convert numeric-like object columns into numeric columns.
    for column in df.select_dtypes(include=["object"]).columns:

        converted = pd.to_numeric(df[column], errors="coerce")

        # Convert only if every non-null value was numeric.
        if converted.notna().sum() == df[column].notna().sum():
            df[column] = converted

    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_summary": {},
    }

    numeric_df = df.select_dtypes(include=np.number)

    if not numeric_df.empty:
        summary["numeric_summary"] = numeric_df.describe().round(2).to_dict()

    return summary


def calculate_percentage_change(current_value: float, previous_value: float) -> float:
    """
    Calculate percentage change between two values.
    """

    if previous_value == 0:
        raise ValueError("Previous value cannot be zero.")

    change = ((current_value - previous_value) / previous_value) * 100

    return round(float(change), 2)


def group_and_aggregate(
    df: pd.DataFrame, group_by: str, metric: str, aggregation: str = "sum"
) -> pd.DataFrame:
    """
    Group data and perform a supported aggregation.
    """

    allowed_aggregations = {"sum", "mean", "min", "max", "count"}

    if aggregation not in allowed_aggregations:
        raise ValueError("Unsupported aggregation operation.")

    if group_by not in df.columns:
        raise ValueError(f"Column not found: {group_by}")

    if metric not in df.columns:
        raise ValueError(f"Column not found: {metric}")

    result = df.groupby(group_by)[metric].agg(aggregation).reset_index()

    return result
