import sqlglot
from sqlglot import exp

ALLOWED_TABLES = {
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
    "returns",
    "inventory",
}

ALLOWED_SCHEMAS = {"", "public"}

BLOCKED_FUNCTIONS = {
    "pg_sleep",
    "pg_read_file",
    "pg_read_binary_file",
    "pg_ls_dir",
    "pg_write_file",
    "lo_import",
    "lo_export",
    "dblink",
    "dblink_exec",
    "set_config",
}

BLOCKED_STATEMENTS = {
    "insert",
    "update",
    "delete",
    "merge",
    "create",
    "drop",
    "alter",
    "truncate",
    "command",
    "copy",
}


def validate_sql(sql: str) -> bool:

    if not sql or not sql.strip():
        raise ValueError("SQL query cannot be empty.")

    if len(sql) > 20000:
        raise ValueError("SQL query exceeds the maximum allowed length.")

    try:
        # Parse SQL using PostgreSQL dialect
        parsed_queries = sqlglot.parse(sql, read="postgres")

        # Reject multiple statements
        if len(parsed_queries) != 1:
            raise ValueError("Multiple SQL statements are not allowed.")

        query = parsed_queries[0]

        if query is None:
            raise ValueError("Invalid SQL query.")

        # Only SELECT / query expressions are permitted
        if not isinstance(query, exp.Query):
            raise ValueError("Only SELECT queries are allowed.")

        # Reject SELECT INTO, including nested SELECT statements
        for select in query.find_all(exp.Select):
            if select.args.get("into") is not None:
                raise ValueError("SELECT INTO is not allowed.")

        # Reject data modification statements inside CTEs or subqueries
        for node in query.walk():
            if node.__class__.__name__.lower() in BLOCKED_STATEMENTS:
                raise ValueError(
                    "Data modification and administrative statements are not allowed."
                )

        # Identify CTE names
        cte_names = {cte.alias_or_name.lower() for cte in query.find_all(exp.CTE)}

        # Identify actual database tables
        referenced_tables = set()

        for table in query.find_all(exp.Table):

            table_name = table.name.lower()
            schema_name = (table.db or "").lower()
            catalog_name = (table.catalog or "").lower()

            # Reject references outside the permitted schema
            if schema_name not in ALLOWED_SCHEMAS:
                raise ValueError(f"Unauthorized database schema: {schema_name}")

            if catalog_name:
                raise ValueError("Cross-database references are not allowed.")

            # Ignore CTE references
            if table_name not in cte_names:
                referenced_tables.add(table_name)

        # Reject unauthorized tables
        unauthorized = referenced_tables - ALLOWED_TABLES

        if unauthorized:
            raise ValueError(f"Unauthorized tables: {unauthorized}")

        # Reject dangerous PostgreSQL functions
        for function in query.find_all(exp.Func):

            if isinstance(function, exp.Anonymous):
                function_name = function.name.lower()
            else:
                function_name = function.sql_name().lower()

            if function_name in BLOCKED_FUNCTIONS:
                raise ValueError(f"SQL function '{function_name}' is not allowed.")

        return True

    except sqlglot.errors.ParseError as error:
        raise ValueError(f"Invalid SQL syntax: {error}") from error
