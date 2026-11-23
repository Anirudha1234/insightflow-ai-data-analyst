import pandas as pd

from app.tools.python_analyzer import get_dataframe_summary, group_and_aggregate


def python_analysis_node(state: dict) -> dict:

    try:

        df = state["dataframe"]

        if df is None or df.empty:
            return {"python_analysis": {}, "status": "success"}

        analysis_results = {}

        # 1. Statistical summary
        analysis_results["summary"] = get_dataframe_summary(df)

        # 2. Correlation analysis
        numeric_df = df.copy()

        for column in numeric_df.columns:

            if numeric_df[column].dtype == "object":

                converted = pd.to_numeric(numeric_df[column], errors="coerce")

                if converted.notna().sum() == numeric_df[column].notna().sum():
                    numeric_df[column] = converted

        numeric_columns = numeric_df.select_dtypes(include="number").columns.tolist()

        # Exclude identifier columns
        numeric_columns = [
            column
            for column in numeric_columns
            if column.lower() != "id" and not column.lower().endswith("_id")
        ]

        if len(numeric_columns) >= 2:

            correlation = numeric_df[numeric_columns].corr()

            analysis_results["correlation"] = correlation.round(4).to_dict()

        else:

            analysis_results["correlation"] = None

        return {"python_analysis": analysis_results, "status": "success"}

    except Exception as error:

        return {"python_analysis": {}, "error": str(error), "status": "error"}
