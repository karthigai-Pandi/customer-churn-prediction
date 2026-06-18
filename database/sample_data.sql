-- Sample data for testing
USE customer_churn_db;

-- Insert sample users
INSERT INTO users (username, email, password_hash, full_name, is_active) VALUES
('admin', 'admin@churnprediction.com', 'pbkdf2:sha256:600000$hash123$admin', 'Admin User', TRUE),
('analyst1', 'analyst@churnprediction.com', 'pbkdf2:sha256:600000$hash123$analyst', 'Data Analyst', TRUE),
('manager1', 'manager@churnprediction.com', 'pbkdf2:sha256:600000$hash123$manager', 'Manager', TRUE);

-- Insert sample customers
INSERT INTO customers (contract_id, gender, age, tenure_months, phone_service, internet_service, online_security, 
online_backup, device_protection, tech_support, streaming_tv, streaming_movies, contract, paperless_billing, 
payment_method, monthly_charges, total_charges) VALUES
('CUST001', 'Male', 65, 2, 'No', 'Fiber optic', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Month-to-month', 'Yes', 'Credit card', 70.70, 1397.00),
('CUST002', 'Female', 25, 34, 'Yes', 'DSL', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'One year', 'No', 'Bank transfer', 56.15, 1896.00),
('CUST003', 'Male', 45, 65, 'Yes', 'Cable', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'Two year', 'Yes', 'Credit card', 64.99, 4225.00),
('CUST004', 'Female', 35, 12, 'No', 'Fiber optic', 'No', 'No', 'No', 'No', 'No', 'No', 'Month-to-month', 'Yes', 'Electronic check', 75.80, 908.00),
('CUST005', 'Male', 55, 48, 'Yes', 'DSL', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No', 'One year', 'No', 'Bank transfer', 45.50, 2184.00),
('CUST006', 'Female', 30, 6, 'Yes', 'Cable', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'Month-to-month', 'Yes', 'Credit card', 59.99, 360.00),
('CUST007', 'Male', 60, 72, 'No', 'DSL', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'Two year', 'No', 'Bank transfer', 51.25, 3690.00),
('CUST008', 'Female', 28, 3, 'Yes', 'Fiber optic', 'No', 'No', 'Yes', 'No', 'No', 'No', 'Month-to-month', 'Yes', 'Electronic check', 82.50, 247.50),
('CUST009', 'Male', 50, 40, 'Yes', 'Cable', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'One year', 'No', 'Credit card', 68.75, 2750.00),
('CUST010', 'Female', 42, 20, 'No', 'DSL', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'Month-to-month', 'Yes', 'Bank transfer', 48.50, 970.00);

-- Insert sample predictions
INSERT INTO predictions (customer_id, user_id, contract_id, churn_prediction, churn_probability, risk_level, 
model_name, confidence_score, notes) VALUES
(1, 1, 'CUST001', 1, 0.8750, 'High Risk', 'Random Forest', 0.95, 'High churn probability due to short tenure'),
(2, 1, 'CUST002', 0, 0.2100, 'Low Risk', 'Random Forest', 0.92, 'Low churn risk with long tenure'),
(3, 1, 'CUST003', 0, 0.1850, 'Low Risk', 'Random Forest', 0.94, 'Stable customer with long tenure'),
(4, 2, 'CUST004', 1, 0.7650, 'High Risk', 'Random Forest', 0.91, 'Short tenure with fiber optic service'),
(5, 2, 'CUST005', 0, 0.3200, 'Low Risk', 'Random Forest', 0.93, 'Good services usage pattern'),
(6, 2, 'CUST006', 1, 0.6800, 'High Risk', 'Random Forest', 0.89, 'Very new customer with month-to-month contract'),
(7, 3, 'CUST007', 0, 0.1500, 'Low Risk', 'Random Forest', 0.96, 'Very stable long-term customer'),
(8, 3, 'CUST008', 1, 0.9200, 'High Risk', 'Random Forest', 0.94, 'Extremely short tenure increases risk'),
(9, 3, 'CUST009', 0, 0.2750, 'Low Risk', 'Random Forest', 0.90, 'Good service adoption'),
(10, 1, 'CUST010', 1, 0.5480, 'Medium Risk', 'Random Forest', 0.88, 'Moderate risk profile');

-- Insert model performance metrics
INSERT INTO model_performance (model_name, accuracy, precision, recall, f1_score, roc_auc, data_size, is_best_model) VALUES
('Logistic Regression', 0.7950, 0.6480, 0.5620, 0.6010, 0.8560, 7043, FALSE),
('Decision Tree', 0.7450, 0.5890, 0.6150, 0.6010, 0.7420, 7043, FALSE),
('Random Forest', 0.8050, 0.6720, 0.5940, 0.6310, 0.8720, 7043, TRUE),
('XGBoost', 0.7980, 0.6520, 0.5810, 0.6150, 0.8650, 7043, FALSE);
