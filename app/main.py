from pathlib import Path

import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from app.agents.graph import analyst_graph
from app.api.schemas import AnalyzeRequest, AnalyzeResponse

import os

app = FastAPI(
    title="InsightFlow AI Data Analyst",
    description="AI-powered natural-language data analysis API",
    version="1.0.0",
)

# CORS configuration
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory where generated Plotly charts are stored
DATA_DIR = Path("data").resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "InsightFlow AI Data Analyst"}


@app.get("/charts/{filename}")
def get_chart(filename: str):

    # Only allow HTML chart filenames, not directory traversal
    if Path(filename).name != filename or not filename.endswith(".html"):
        raise HTTPException(status_code=400, detail="Invalid chart filename")

    chart_file = (DATA_DIR / filename).resolve()

    if not chart_file.is_relative_to(DATA_DIR) or not chart_file.is_file():
        raise HTTPException(status_code=404, detail="Chart not found")

    return FileResponse(
        path=chart_file,
        media_type="text/html",
    )


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_data(request: AnalyzeRequest):

    try:
        # Run the LangGraph workflow
        result = analyst_graph.invoke({"question": request.question})

        # Convert DataFrame results into JSON-safe records
        dataframe = result.get("dataframe")

        if isinstance(dataframe, pd.DataFrame):
            safe_df = dataframe.astype(object).where(pd.notna(dataframe), None)
            records = safe_df.to_dict(orient="records")
        else:
            records = []

        response = AnalyzeResponse(
            question=request.question,
            answer=result.get("answer"),
            sql_query=result.get("sql_query"),
            results=jsonable_encoder(records),
            calculations=jsonable_encoder(result.get("calculations") or {}),
            chart_required=bool(result.get("chart_required", False)),
            chart_type=result.get("chart_type"),
            chart_path=result.get("chart_path"),
            status=result.get("status", "error"),
            error=result.get("error"),
        )

        return response

    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Analysis failed: {str(error)}"
        ) from error
