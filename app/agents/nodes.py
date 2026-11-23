from app.services.sql_generator import generate_sql
from app.tools.sql_executor import execute_sql
from app.tools.python_analyzer import get_dataframe_summary
from app.services.gemini_client import generate_response


def generate_sql_node(state: dict) -> dict:

    try:
        question = state["question"]
        sql = generate_sql(question)

        return {"sql_query": sql, "error": None, "status": "success"}

    except Exception as error:

        return {"error": str(error), "status": "error"}


def execute_sql_node(state: dict) -> dict:

    try:
        sql = state["sql_query"]
        df = execute_sql(sql)

        return {"dataframe": df, "error": None, "status": "success"}

    except Exception as error:

        return {"error": str(error), "status": "error"}


def analyze_data_node(state: dict) -> dict:

    try:
        df = state["dataframe"]
        analysis = get_dataframe_summary(df)

        return {"analysis": analysis, "status": "success"}

    except Exception as error:

        return {"error": str(error), "status": "error"}


def generate_answer_node(state: dict) -> dict:
    try:
        question = state["question"]
        sql = state["sql_query"]
        df = state["dataframe"]

        analysis = state.get("analysis", {})
        python_analysis = state.get("python_analysis", {})
        calculations = state.get("calculations", {})

        prompt = f"""
You are an expert AI Data Analyst.

Answer the user's business question using only the SQL results,
Python analysis, and calculator results provided below.

USER QUESTION:
{question}

GENERATED SQL:
{sql}

QUERY RESULTS:
{df.to_string(index=False)}

SQL DATA ANALYSIS:
{analysis}

PYTHON ANALYSIS:
{python_analysis}

CALCULATOR RESULTS:
{calculations}

AUTHORITATIVE CALCULATION RULE:

Calculator results have priority over raw SQL values
for any metric they contain.

Examples:
- percentage: 70.33 means write 70.33%, NOT 70.3288%.
- revenue_growth: 42.91 means write 42.91%.
- average_order_value: 65592.52 means write 65592.52.

Never display the unrounded SQL value for a metric
already present in calculator results.

CURRENCY AND UNIT RULE — STRICT:

The database schema does not define a currency.

Therefore:
- NEVER use $, USD, ₹, INR, £, € or any other currency symbol
  unless the user explicitly specifies the currency or the
  supplied data explicitly identifies it.
- Display revenue and monetary-looking values as plain numbers.
- Do not assume that a number represents dollars or rupees.
- Do not invent measurement units.
- Percentages may use % when the metric is a percentage.

Correct: Delivered revenue was 56,069,849.88.
Incorrect: Delivered revenue was $56,069,849.88.
Incorrect: Delivered revenue was ₹56,069,849.88.

INSTRUCTIONS:

1. Directly answer the user's business question.
2. Highlight the most important findings.
3. Use exact figures from supplied results.
4. Prioritize calculator results for calculated metrics.
5. Do not contradict or unnecessarily recalculate calculator results.
6. Use Python analysis for useful statistical findings.
7. Do not interpret correlation as causation.
8. Do not describe a completed year as "so far".
9. Clearly distinguish gross revenue from net revenue.
10. Do not claim returns or refunds are excluded unless SQL
    explicitly handles them.
11. Explain the business meaning of the results.
12. Do not invent unsupported conclusions.
13. If information is insufficient, clearly mention it.
14. Format the answer using readable Markdown.
15. Keep the response concise and business-focused.

IMPORTANT:
- SQL results are the source of truth for database figures.
- Calculator results are the source of truth for calculated metrics.
- Python analysis provides supporting statistical insights.
- Never invent currency symbols or units.
- Ignore irrelevant analysis fields.
"""

        answer = generate_response(prompt)

        return {"answer": answer, "error": None, "status": "success"}

    except Exception as error:
        return {"error": str(error), "status": "error"}
