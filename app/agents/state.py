from typing import TypedDict, Optional, Any


class AnalystState(TypedDict):

    question: str

    sql_query: Optional[str]

    dataframe: Optional[Any]

    # Existing data analysis summary
    analysis: Optional[dict]

    # New: advanced Python analysis results
    python_analysis: Optional[dict]

    # New: calculator results
    calculations: Optional[dict]

    # Chart information
    chart_path: Optional[str]

    chart_type: Optional[str]

    chart_required: Optional[bool]

    # Final response
    answer: Optional[str]

    error: Optional[str]

    status: Optional[str]
