-- Philippine payment gateway schema
-- CREATE DATABASE thinkbit_payments;

\c thinkbit_payments;

-- Create ENUM types for Philippine payment methods
CREATE TYPE payment_method AS ENUM ('GCASH', 'PAYMAYA');
CREATE TYPE txn_status AS ENUM ('PENDING', 'COMPLETED', 'FAILED');

-- Create transactions table with PH context
CREATE TABLE transactions (
    id VARCHAR(36) PRIMARY KEY,
    payment_method payment_method NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency CHAR(3) DEFAULT 'PHP',
    status txn_status DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample Philippine transactions
INSERT INTO transactions (id, payment_method, amount, status) VALUES
('PH-TXN-20250725-001', 'GCASH', 1500.00, 'COMPLETED'),
('PH-TXN-20250725-002', 'PAYMAYA', 2500.50, 'COMPLETED'),
('PH-TXN-20250725-003', 'GCASH', 800.75, 'FAILED'),
('PH-TXN-20250725-004', 'GCASH', 3200.00, 'COMPLETED');