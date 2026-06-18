-- Customer Churn Prediction Database Schema
-- Drop existing database if it exists (optional)
DROP DATABASE IF EXISTS customer_churn_db;

-- Create database
CREATE DATABASE customer_churn_db;
USE customer_churn_db;

-- Create users table (for login functionality)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Create customers table
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id VARCHAR(50) UNIQUE NOT NULL,
    gender VARCHAR(10),
    age INT,
    tenure_months INT,
    phone_service VARCHAR(10),
    internet_service VARCHAR(50),
    online_security VARCHAR(10),
    online_backup VARCHAR(10),
    device_protection VARCHAR(10),
    tech_support VARCHAR(10),
    streaming_tv VARCHAR(10),
    streaming_movies VARCHAR(10),
    contract VARCHAR(50),
    paperless_billing VARCHAR(10),
    payment_method VARCHAR(50),
    monthly_charges DECIMAL(10, 2),
    total_charges DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_contract_id (contract_id),
    INDEX idx_gender (gender),
    INDEX idx_internet_service (internet_service)
);

-- Create predictions table
CREATE TABLE predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    user_id INT,
    contract_id VARCHAR(50),
    churn_prediction INT,
    churn_probability DECIMAL(5, 4),
    risk_level VARCHAR(20),
    model_name VARCHAR(100),
    confidence_score DECIMAL(5, 4),
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_customer_id (customer_id),
    INDEX idx_user_id (user_id),
    INDEX idx_prediction_timestamp (prediction_timestamp),
    INDEX idx_risk_level (risk_level)
);

-- Create model_performance table
CREATE TABLE model_performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    accuracy DECIMAL(5, 4),
    precision DECIMAL(5, 4),
    recall DECIMAL(5, 4),
    f1_score DECIMAL(5, 4),
    roc_auc DECIMAL(5, 4),
    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_size INT,
    is_best_model BOOLEAN DEFAULT FALSE,
    INDEX idx_model_name (model_name),
    INDEX idx_is_best (is_best_model)
);

-- Create audit_log table
CREATE TABLE audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100),
    table_name VARCHAR(50),
    record_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- Create statistics table
CREATE TABLE statistics (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value DECIMAL(15, 4),
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    INDEX idx_metric_name (metric_name),
    INDEX idx_calculation_date (calculation_date)
);
