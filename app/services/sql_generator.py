from app.services.gemini_client import generate_response
from app.database.schema_context import DATABASE_SCHEMA

SQL_GENERATION_PROMPT = """
You are an expert PostgreSQL query generator.

Your task is to convert the user's business question into
a valid PostgreSQL SELECT query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

STRICT RULES:

1. Generate only SELECT queries.
2. Do not generate INSERT, UPDATE, DELETE, DROP,
   ALTER, CREATE, TRUNCATE or other write operations.
3. Do not generate multiple SQL statements.
4. Use only tables and columns from the provided schema.
5. Use correct JOIN conditions.
6. Use PostgreSQL-compatible syntax.
7. Add meaningful column aliases.
8. Limit large result sets to 100 rows unless the
   question explicitly requests a smaller limit.
9. Do not invent data or table names.
10. Return only SQL. No Markdown fences or explanations.

SQL QUERY:
"""


def generate_sql(question: str) -> str:
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    prompt = SQL_GENERATION_PROMPT.format(
        schema=DATABASE_SCHEMA, question=question.strip()
    )

    sql = generate_response(prompt)

    # Remove Markdown fences if the model adds them.
    sql = sql.strip()

    if sql.startswith("```"):
        sql = sql.replace("```sql", "", 1)
        sql = sql.replace("```", "").strip()

    return sql.rstrip(";").strip()
