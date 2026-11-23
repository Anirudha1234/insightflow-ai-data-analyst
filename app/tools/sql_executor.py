import pandas as pd

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import readonly_engine
from app.tools.sql_validator import validate_sql

MAX_RESULT_ROWS = 100


def execute_sql(sql: str) -> pd.DataFrame:

    # Validate SQL before execution
    validate_sql(sql)

    try:
        with readonly_engine.connect() as connection:

            result = connection.execute(text(sql))

            columns = result.keys()

            # Fetch at most 101 rows to detect oversized results
            rows = result.fetchmany(MAX_RESULT_ROWS + 1)

            if len(rows) > MAX_RESULT_ROWS:
                raise ValueError(
                    f"Query returned more than {MAX_RESULT_ROWS} rows. "
                    "Please refine your query or add a LIMIT clause."
                )

            return pd.DataFrame(rows, columns=columns)

    except SQLAlchemyError as error:
        raise RuntimeError(f"Database query execution failed: {error}") from error
