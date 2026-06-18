# Project Implementation Guide

Complete guide for deploying and using the Customer Churn Prediction application.

## Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] MySQL Server 5.7 or higher installed
- [ ] Git installed
- [ ] Kaggle account (for dataset)
- [ ] Text editor or IDE (VS Code, PyCharm, etc.)
- [ ] Internet connection

## Installation & Setup

### Step 1: Environment Setup

```bash
# Windows Command Prompt / macOS Terminal / Linux Bash

# Navigate to project directory
cd customer_churn_prediction

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### Step 2: Database Configuration

```bash
# Open MySQL command line
mysql -u root -p

# Enter your MySQL password
# Then run in MySQL prompt:
```

```sql
-- Create database
CREATE DATABASE customer_churn_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use database
USE customer_churn_db;

-- Source schema file
SOURCE path/to/database/schema.sql;

-- Source sample data
SOURCE path/to/database/sample_data.sql;

-- Verify tables created
SHOW TABLES;
-- Output: users, customers, predictions, model_performance, audit_log, statistics

-- Exit MySQL
EXIT;
```

### Step 3: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings (using your favorite editor)
# nano .env (Linux/Mac)
# notepad .env (Windows)
```

**Important .env settings**:

```
# Flask Configuration
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=your-secret-key-change-this

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_DB=customer_churn_db

# Application Configuration
DEBUG=True
```

### Step 4: Download Dataset

**Option A: Manual Download**

1. Go to https://www.kaggle.com/datasets/blastchar/telco-customer-churn
2. Click "Download"
3. Extract to `data/` folder
4. Rename file to `WA_Fn-UseC_-Telco-Customer-Churn.csv`

**Option B: Using Kaggle API**

```bash
# Install kaggle
pip install kaggle

# Configure API credentials
# Create ~/.kaggle/kaggle.json with your API key
# https://github.com/Kaggle/kaggle-api#api-credentials

# Download dataset
kaggle datasets download -d blastchar/telco-customer-churn -p data/

# Unzip
unzip data/telco-customer-churn.zip -d data/

# Remove zip
rm data/telco-customer-churn.zip
```

**Verify Dataset**:

```bash
ls -la data/
# Should show: WA_Fn-UseC_-Telco-Customer-Churn.csv
```

## Training the ML Model

```bash
# Navigate to ML pipeline directory
cd ml_pipeline

# Run training script
python train_pipeline.py

# Expected output:
# Data loaded successfully. Shape: (7043, 21)
# Data preparation completed...
# Training all models...
# Logistic Regression trained successfully
# Decision Tree trained successfully
# Random Forest trained successfully
# XGBoost trained successfully
# Evaluating all models...
# Best model: Random Forest (ROC-AUC: 0.8720)
# Models saved to ../models
```

**Generated Files**:

- `../models/best_model.pkl` - Trained Random Forest model
- `../models/scaler.pkl` - Feature scaler
- `../models/encoder.pkl` - Categorical encoder
- `../models/feature_columns.pkl` - Feature list
- `../models/training_report.txt` - Performance metrics
- `../eda_report/` - EDA visualizations

## Running the Application

### Development Server

```bash
# From project root directory (not in ml_pipeline)
cd ..

# Run Flask application
python run.py

# Output:
# ================================================================================
# Customer Churn Prediction Web Application
# ================================================================================
# Running on: http://127.0.0.1:5000
# Debug mode: True
# ================================================================================
```

**Access Application**:

- Web UI: http://localhost:5000/auth/login
- Default credentials: username `admin`, password `admin123`

### Production Server

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# With more workers for high load
gunicorn -w 8 -b 0.0.0.0:5000 --timeout 120 run:app
```

## Using the Application

### Login & Navigation

1. **Login Page** (`/auth/login`)
   - Enter: `admin` / `admin123`
   - Click "Login"

2. **Dashboard** (`/dashboard/`)
   - View statistics
   - See recent predictions
   - Quick access links

3. **Make Predictions** (`/predict/`)
   - Fill customer information
   - Click "Make Prediction"
   - View result

4. **Prediction History** (`/predict/history`)
   - View all predictions
   - Filter and search
   - Export data

5. **Customer Management** (`/customer/`)
   - View all customers
   - Add new customer
   - Search customers

6. **Analytics** (`/analytics/`)
   - Model performance
   - Risk distribution charts
   - Churn statistics

### Making a Prediction

**Form Fields**:

- Contract ID (required): e.g., `CUST001`
- Tenure (months): 12-72
- Internet Service: DSL, Fiber optic, Cable, No
- Monthly Charges: e.g., 65.50
- Total Charges: e.g., 786.00
- Other services: Yes/No options

**Result Interpretation**:

- **Churn Prediction**: Will/Won't Churn
- **Probability**: Percentage likelihood (0-100%)
- **Risk Level**: High Risk / Low Risk
- **Confidence**: Model confidence (0-1)

### Exporting Data

```bash
# Export predictions as CSV
curl -X GET "http://localhost:5000/api/export/predictions?format=csv" \
  -H "X-API-Key: demo-key-12345" \
  -o predictions.csv

# Export as PDF
curl -X GET "http://localhost:5000/api/export/predictions?format=pdf" \
  -H "X-API-Key: demo-key-12345" \
  -o predictions.pdf
```

## REST API Usage

### Health Check

```bash
curl http://localhost:5000/api/health

# Response:
# {
#   "status": "healthy",
#   "timestamp": "2026-06-18T10:30:00",
#   "database": "connected",
#   "model": "loaded"
# }
```

### Make Prediction via API

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "X-API-Key: demo-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": "CUST001",
    "tenure_months": 12,
    "monthly_charges": 65.5,
    "total_charges": 786.0,
    "internet_service": "Fiber optic",
    "phone_service": "Yes",
    "contract": "Month-to-month",
    "save_prediction": true
  }'
```

### Get Predictions

```bash
# Get all predictions (limit 10)
curl -X GET "http://localhost:5000/api/predictions?limit=10" \
  -H "X-API-Key: demo-key-12345"

# Get high-risk predictions
curl -X GET "http://localhost:5000/api/predictions?risk_level=High Risk" \
  -H "X-API-Key: demo-key-12345"
```

## Troubleshooting

### Issue: MySQL Connection Error

```
Error: MySQL connection refused
```

**Solutions**:

1. Check MySQL is running:

   ```bash
   # Windows
   mysql --version

   # macOS
   brew services list | grep mysql

   # Linux
   sudo systemctl status mysql
   ```

2. Verify credentials in `.env`:

   ```bash
   mysql -h localhost -u root -p
   ```

3. Check database exists:
   ```bash
   mysql -u root -p -e "SHOW DATABASES;" | grep customer_churn_db
   ```

### Issue: Model Files Not Found

```
Error: Model file not found at models/best_model.pkl
```

**Solutions**:

1. Check models directory:

   ```bash
   ls -la models/
   ```

2. Retrain model:

   ```bash
   cd ml_pipeline
   python train_pipeline.py
   ```

3. Verify dataset exists:
   ```bash
   ls -la data/WA_Fn-UseC_-Telco-Customer-Churn.csv
   ```

### Issue: Static Files Not Loading (CSS/JS)

```
404 Not Found: /static/css/style.css
```

**Solutions**:

1. Verify static folder exists:

   ```bash
   ls -la app/static/
   ```

2. Restart Flask application

3. Clear browser cache (Ctrl+Shift+Delete)

4. Check Flask configuration:
   ```python
   app = Flask(__name__, static_folder='static')
   ```

### Issue: Port Already in Use

```
Address already in use: ('127.0.0.1', 5000)
```

**Solutions**:

```bash
# Use different port
python run.py --port 5001

# Or edit run.py:
app.run(host='127.0.0.1', port=8000)

# Or kill existing process:
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

## Testing the Application

### Manual Testing

```bash
# Test login
curl -X POST http://localhost:5000/auth/login \
  -d "username=admin&password=admin123"

# Test prediction API
curl -X POST http://localhost:5000/api/predict \
  -H "X-API-Key: demo-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"contract_id":"TEST001","tenure_months":12,"monthly_charges":65,"total_charges":780,"internet_service":"DSL"}'

# Test database query
mysql -u root -p customer_churn_db -e "SELECT COUNT(*) FROM predictions;"
```

### Test Data Creation

```bash
# Insert test customer
mysql -u root -p customer_churn_db -e "
INSERT INTO customers (contract_id, gender, age, tenure_months, internet_service, monthly_charges, total_charges)
VALUES ('TEST_CUST', 'Male', 45, 24, 'DSL', 65.5, 1572);
"

# Insert test prediction
mysql -u root -p customer_churn_db -e "
INSERT INTO predictions (contract_id, churn_prediction, churn_probability, risk_level, model_name, confidence_score)
VALUES ('TEST_CUST', 0, 0.35, 'Low Risk', 'Random Forest', 0.92);
"
```

## Performance Optimization

### Enable Query Caching

```sql
-- Check cache status
SHOW VARIABLES LIKE 'query_cache%';

-- Enable caching (MySQL < 5.7)
SET GLOBAL query_cache_type = 1;
SET GLOBAL query_cache_size = 268435456;  # 256MB
```

### Optimize Slow Queries

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Check slow queries
SHOW PROCESSLIST;
```

### Database Maintenance

```sql
-- Analyze tables
ANALYZE TABLE users, customers, predictions;

-- Optimize tables
OPTIMIZE TABLE customers, predictions;

-- Check table status
CHECK TABLE customers;
```

## Security Checklist

- [ ] Changed `SECRET_KEY` in .env
- [ ] Changed MySQL root password
- [ ] Set `DEBUG=False` in production
- [ ] Configured HTTPS/SSL
- [ ] Set strong API keys
- [ ] Enabled firewalls
- [ ] Regular backups enabled
- [ ] Log monitoring enabled

## Backup & Recovery

### Database Backup

```bash
# Backup database
mysqldump -u root -p customer_churn_db > backup_$(date +%Y%m%d).sql

# Restore from backup
mysql -u root -p customer_churn_db < backup_20260618.sql
```

### Model Backup

```bash
# Backup trained models
cp -r models/ models_backup/

# Restore models
cp -r models_backup/* models/
```

## Monitoring

### Check Application Health

```bash
# Check Flask logs
tail -f logs/flask.log

# Check database performance
mysql> SHOW PROCESSLIST;
mysql> SHOW STATUS LIKE '%connections%';

# Check system resources
# Windows
Get-Process python

# macOS/Linux
ps aux | grep python
top -p $(pgrep -f "python run.py")
```

### Monitor Predictions

```sql
-- Count daily predictions
SELECT DATE(prediction_timestamp) as date, COUNT(*) as count
FROM predictions
GROUP BY DATE(prediction_timestamp)
ORDER BY date DESC;

-- Check model distribution
SELECT model_name, COUNT(*) as usage
FROM predictions
GROUP BY model_name;

-- Analyze churn distribution
SELECT churn_prediction, COUNT(*) as count, ROUND(COUNT(*)*100/TOTAL, 2) as percentage
FROM predictions
CROSS JOIN (SELECT COUNT(*) as TOTAL FROM predictions) t
GROUP BY churn_prediction;
```

## Next Steps

1. ✅ Set up development environment
2. ✅ Train ML models
3. ✅ Run Flask application
4. ✅ Test with sample data
5. 📝 Create more test predictions
6. 🔄 Monitor application performance
7. 🚀 Deploy to production (Render, AWS, etc.)
8. 📊 Set up monitoring & alerting
9. 🔐 Implement additional security
10. 📈 Collect feedback and iterate

---

**Implementation Guide Version**: 1.0  
**Last Updated**: June 2026  
**Status**: Complete ✅
