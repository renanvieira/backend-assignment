CREATE TABLE customers (
    id INT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_number TEXT UNIQUE,
    price_amount BIGINT NOT NULL CONSTRAINT order_price_positive CHECK (price_amount > 0),
    status TEXT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,

    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE tickets (
    id INT PRIMARY KEY,
    order_id INT,
    barcode TEXT NOT NULL,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT uq_order_barcode UNIQUE (order_id, barcode)
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);

