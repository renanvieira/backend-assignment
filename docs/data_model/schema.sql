CREATE TABLE customers (
    id INT PRIMARY KEY,
    -- In a real system, we would have name, email, etc.
    email VARCHAR(255) UNIQUE
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE barcodes (
    barcode VARCHAR(255) PRIMARY KEY,
    order_id INT UNIQUE,
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
