
-- =========================================
-- INSIGHTFLOW: E-COMMERCE DATABASE
-- =========================================

-- 1. CUSTOMERS
CREATE TABLE customers (
    customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- 2. PRODUCTS
CREATE TABLE products (
    product_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    cost_price NUMERIC(12, 2) NOT NULL CHECK (cost_price >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CHECK (cost_price <= price)
);


-- 3. ORDERS
CREATE TABLE orders (
    order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    order_status VARCHAR(30) NOT NULL
        CHECK (
            order_status IN (
                'pending',
                'confirmed',
                'shipped',
                'delivered',
                'cancelled'
            )
        ),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- 4. ORDER ITEMS
CREATE TABLE order_items (
    order_item_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    UNIQUE (order_id, product_id)
);


-- 5. PAYMENTS
CREATE TABLE payments (
    payment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL,
    payment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount >= 0),
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(30) NOT NULL
        CHECK (
            payment_status IN (
                'pending',
                'completed',
                'failed',
                'refunded'
            )
        ),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- 6. RETURNS
CREATE TABLE returns (
    return_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_item_id BIGINT NOT NULL,
    return_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    return_reason VARCHAR(255),
    refund_amount NUMERIC(12, 2) NOT NULL
        CHECK (refund_amount >= 0),

    FOREIGN KEY (order_item_id)
        REFERENCES order_items(order_item_id)
);


-- 7. INVENTORY
CREATE TABLE inventory (
    inventory_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id BIGINT UNIQUE NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0
        CHECK (stock_quantity >= 0),
    reorder_level INTEGER NOT NULL DEFAULT 10
        CHECK (reorder_level >= 0),
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


-- =========================================
-- INDEXES FOR QUERY PERFORMANCE
-- =========================================

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_orders_date
ON orders(order_date);

CREATE INDEX idx_orders_status
ON orders(order_status);

CREATE INDEX idx_order_items_product
ON order_items(product_id);

CREATE INDEX idx_payments_order
ON payments(order_id);

CREATE INDEX idx_returns_order_item
ON returns(order_item_id);

CREATE INDEX idx_products_category
ON products(category);
