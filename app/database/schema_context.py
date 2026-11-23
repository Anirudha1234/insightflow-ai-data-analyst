DATABASE_SCHEMA = """
You are working with a PostgreSQL e-commerce database.

TABLE: customers
- customer_id: BIGINT, primary key
- first_name: VARCHAR
- last_name: VARCHAR
- email: VARCHAR
- city: VARCHAR
- state: VARCHAR
- created_at: TIMESTAMP

TABLE: products
- product_id: BIGINT, primary key
- product_name: VARCHAR
- category: VARCHAR
- price: NUMERIC
- cost_price: NUMERIC
- is_active: BOOLEAN
- created_at: TIMESTAMP

TABLE: orders
- order_id: BIGINT, primary key
- customer_id: BIGINT, foreign key -> customers.customer_id
- order_date: TIMESTAMP
- order_status: VARCHAR

TABLE: order_items
- order_item_id: BIGINT, primary key
- order_id: BIGINT, foreign key -> orders.order_id
- product_id: BIGINT, foreign key -> products.product_id
- quantity: INTEGER
- unit_price: NUMERIC

TABLE: payments
- payment_id: BIGINT, primary key
- order_id: BIGINT, foreign key -> orders.order_id
- payment_date: TIMESTAMP
- amount: NUMERIC
- payment_method: VARCHAR
- payment_status: VARCHAR

TABLE: returns
- return_id: BIGINT, primary key
- order_item_id: BIGINT, foreign key -> order_items.order_item_id
- return_date: TIMESTAMP
- quantity: INTEGER
- return_reason: VARCHAR
- refund_amount: NUMERIC

TABLE: inventory
- inventory_id: BIGINT, primary key
- product_id: BIGINT, foreign key -> products.product_id
- stock_quantity: INTEGER
- reorder_level: INTEGER
- last_updated: TIMESTAMP

IMPORTANT BUSINESS RULES:

1. Revenue from delivered orders can be calculated using:
   SUM(order_items.quantity * order_items.unit_price)

2. Only delivered orders should be included when a question
   explicitly asks for delivered-order sales.

3. Order statuses include:
   pending, confirmed, shipped, delivered, cancelled.

4. Payment statuses include:
   pending, completed, failed, refunded.

5. To calculate product revenue, join:
   orders -> order_items -> products.

6. Product transaction prices must come from order_items.unit_price,
   not the current products.price.

7. Returns are stored separately in the returns table.
"""
