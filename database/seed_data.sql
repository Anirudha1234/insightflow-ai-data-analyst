
-- ============================================
-- INSIGHTFLOW: SYNTHETIC E-COMMERCE DATA
-- ============================================

BEGIN;

-- Re-running this script resets the sample data.
TRUNCATE TABLE
    returns,
    payments,
    inventory,
    order_items,
    orders,
    products,
    customers
RESTART IDENTITY CASCADE;

-- Repeatable random data for this session.
SELECT setseed(0.42);


-- ============================================
-- 1. CUSTOMERS: 1000 RECORDS
-- ============================================

INSERT INTO customers (
    first_name,
    last_name,
    email,
    phone,
    city,
    state,
    created_at
)
SELECT
    'Customer',
    'User' || gs,
    'customer' || gs || '@example.com',
    '900000' || LPAD(gs::text, 4, '0'),
    (ARRAY[
        'Bhopal', 'Indore', 'Delhi', 'Mumbai',
        'Pune', 'Bengaluru', 'Jaipur', 'Hyderabad'
    ])[1 + floor(random() * 8)::int],
    (ARRAY[
        'Madhya Pradesh', 'Maharashtra',
        'Delhi', 'Rajasthan', 'Karnataka',
        'Telangana'
    ])[1 + floor(random() * 6)::int],
    TIMESTAMP '2022-01-01'
        + random() * INTERVAL '730 days'
FROM generate_series(1, 1000) AS gs;


-- ============================================
-- 2. PRODUCTS: 50 RECORDS
-- ============================================

WITH product_data AS (
    SELECT
        gs,
        CASE
            WHEN gs <= 10 THEN 'Electronics'
            WHEN gs <= 20 THEN 'Clothing'
            WHEN gs <= 30 THEN 'Home & Kitchen'
            WHEN gs <= 40 THEN 'Books'
            ELSE 'Sports'
        END AS category
    FROM generate_series(1, 50) AS gs
),
priced_products AS (
    SELECT
        gs,
        category,
        category || ' Product ' || gs AS product_name,
        CASE
            WHEN category = 'Electronics'
                THEN 5000 + random() * 70000
            WHEN category = 'Clothing'
                THEN 300 + random() * 4000
            WHEN category = 'Home & Kitchen'
                THEN 500 + random() * 15000
            WHEN category = 'Books'
                THEN 150 + random() * 1500
            ELSE 300 + random() * 10000
        END AS raw_price
    FROM product_data
)
INSERT INTO products (
    product_name,
    category,
    price,
    cost_price
)
SELECT
    product_name,
    category,
    ROUND(raw_price::numeric, 2),
    ROUND(
        (raw_price * (0.45 + random() * 0.25))::numeric,
        2
    )
FROM priced_products;


-- ============================================
-- 3. ORDERS: 23,400 RECORDS
-- January 2024 - October 2026
-- ============================================

WITH months AS (
    SELECT generate_series(
        DATE '2024-01-01',
        DATE '2026-10-01',
        INTERVAL '1 month'
    ) AS month_start
),
generated_orders AS (
    SELECT
        month_start,
        month_start + random() * INTERVAL '1 month'
            AS order_date,
        random() AS status_random
    FROM months
    CROSS JOIN LATERAL generate_series(
        1,
        CASE
            WHEN EXTRACT(YEAR FROM month_start) = 2024
                THEN 500
            WHEN EXTRACT(YEAR FROM month_start) = 2025
                THEN 700
            ELSE 900
        END
    ) AS g(order_number)
)
INSERT INTO orders (
    customer_id,
    order_date,
    order_status
)
SELECT
    1 + floor(random() * 1000)::bigint,
    order_date,
    CASE
        WHEN status_random < 0.75 THEN 'delivered'
        WHEN status_random < 0.83 THEN 'shipped'
        WHEN status_random < 0.88 THEN 'confirmed'
        WHEN status_random < 0.92 THEN 'pending'
        ELSE 'cancelled'
    END
FROM generated_orders;


-- ============================================
-- 4. ORDER ITEMS
-- 1-4 PRODUCTS PER ORDER
-- ============================================

INSERT INTO order_items (
    order_id,
    product_id,
    quantity,
    unit_price
)
SELECT
    o.order_id,
    ((o.order_id * 7 + item_no * 13) % 50) + 1,
    1 + floor(random() * 3)::int,
    p.price
FROM orders o
CROSS JOIN LATERAL generate_series(
    1,
    1 + floor(random() * 4)::int
) AS item(item_no)
JOIN products p
    ON p.product_id =
       ((o.order_id * 7 + item_no * 13) % 50) + 1;


-- ============================================
-- 5. PAYMENTS: ONE PER ORDER
-- ============================================

INSERT INTO payments (
    order_id,
    payment_date,
    amount,
    payment_method,
    payment_status
)
SELECT
    o.order_id,
    o.order_date,
    SUM(oi.quantity * oi.unit_price),
    (ARRAY[
        'UPI', 'Credit Card',
        'Debit Card', 'Net Banking'
    ])[1 + floor(random() * 4)::int],
    CASE
        WHEN o.order_status = 'cancelled'
            THEN 'failed'
        WHEN o.order_status = 'pending'
            THEN 'pending'
        ELSE 'completed'
    END
FROM orders o
JOIN order_items oi
    ON oi.order_id = o.order_id
GROUP BY
    o.order_id,
    o.order_date,
    o.order_status;


-- ============================================
-- 6. RETURNS
-- Approximately 3.5% OF DELIVERED ITEMS
-- ============================================

INSERT INTO returns (
    order_item_id,
    return_date,
    quantity,
    return_reason,
    refund_amount
)
SELECT
    oi.order_item_id,
    o.order_date + INTERVAL '5 days',
    1,
    'Damaged or not as expected',
    oi.unit_price
FROM order_items oi
JOIN orders o
    ON o.order_id = oi.order_id
WHERE
    o.order_status = 'delivered'
    AND random() < 0.035;


-- ============================================
-- 7. INVENTORY: 50 RECORDS
-- ============================================

INSERT INTO inventory (
    product_id,
    stock_quantity,
    reorder_level
)
SELECT
    product_id,
    floor(random() * 200)::int,
    10 + floor(random() * 20)::int
FROM products;


COMMIT;

-- ============================================
-- DATA GENERATION COMPLETE
-- ============================================
