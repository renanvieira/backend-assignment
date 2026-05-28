-- SQL Data Model for Tiqets Assignment

-- Customers table stores primary user information
CREATE TABLE customers (
    id INT PRIMARY KEY,
    -- In a real system, we would have name, email, etc.
    email VARCHAR(255) UNIQUE
);

-- Orders table links customers to their purchase transactions
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Barcodes table stores the physical tickets. 
-- order_id is NULL if the barcode has not been sold yet.
CREATE TABLE barcodes (
    barcode VARCHAR(255) PRIMARY KEY,
    order_id INT,
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Indexes for performance
-- Optimizes the join between orders and barcodes
CREATE INDEX idx_barcodes_order_id ON barcodes(order_id);

-- Optimizes searching for all orders belonging to a customer (used for Top 5 calculation)
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
