from app.tools.sql_validator import validate_sql

test_queries = [
    (
        "Valid SELECT",
        """
        SELECT product_name, price
        FROM products
        LIMIT 5
        """,
    ),
    (
        "Valid JOIN",
        """
        SELECT p.product_name, SUM(oi.quantity)
        FROM products p
        JOIN order_items oi
        ON p.product_id = oi.product_id
        GROUP BY p.product_name
        """,
    ),
    ("DELETE attack", "DELETE FROM customers"),
    ("DROP attack", "DROP TABLE customers"),
    ("UPDATE attack", "UPDATE products SET price = 0"),
    ("Unauthorized table", "SELECT * FROM admin_users"),
    ("Multiple statements", "SELECT * FROM products; DELETE FROM customers"),
    ("SELECT INTO", "SELECT * INTO backup_table FROM orders"),
    ("System schema access", "SELECT * FROM information_schema.tables"),
    ("Dangerous function", "SELECT pg_sleep(10)"),
    ("Cross-database reference", "SELECT * FROM another_db.public.orders"),
]


for name, query in test_queries:

    try:
        result = validate_sql(query)
        print(f"[PASS] {name}: Accepted")

    except ValueError as error:
        print(f"[BLOCKED] {name}: {error}")
