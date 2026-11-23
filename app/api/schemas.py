from typing import Any, Optional
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Natural-language business analysis question",
    )


class AnalyzeResponse(BaseModel):
    question: str
    answer: Optional[str] = None
    sql_query: Optional[str] = None
    results: list[dict[str, Any]] = Field(default_factory=list)
    calculations: dict[str, Any] = Field(default_factory=dict)
    chart_required: bool = False
    chart_type: Optional[str] = None
    chart_path: Optional[str] = None
    status: str
    error: Optional[str] = None
