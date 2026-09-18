CREATE DATABASE IF NOT EXISTS risk_analytics_db;
USE risk_analytics_db;

-- Dimension: Customers
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    signup_date DATE,
    country VARCHAR(50),
    account_status VARCHAR(20)
);

-- Dimension: Vendors
CREATE TABLE IF NOT EXISTS dim_vendors (
    vendor_id INT PRIMARY KEY,
    vendor_name VARCHAR(100),
    vendor_category VARCHAR(50),
    risk_rating VARCHAR(20)
);

-- Dimension: Dates
CREATE TABLE IF NOT EXISTS dim_dates (
    date_key DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT,
    day_of_week VARCHAR(15)
);

-- Fact Table: Transactions & Risk Logs
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id INT,
    vendor_id INT,
    transaction_date DATE,
    amount DECIMAL(12, 2),
    payment_method VARCHAR(30),
    is_flagged_anomaly INT,
    anomaly_score FLOAT,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (vendor_id) REFERENCES dim_vendors(vendor_id),
    FOREIGN KEY (transaction_date) REFERENCES dim_dates(date_key)
);

-- Audit / Error Logging Table
CREATE TABLE IF NOT EXISTS pipeline_error_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    error_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_name VARCHAR(100),
    error_message TEXT,
    rows_affected INT
);