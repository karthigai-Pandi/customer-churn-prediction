# Customer Churn Prediction - Complete Setup Guide

Complete step-by-step guide to set up and run the application.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [Usage Guide](#usage-guide)
5. [API Reference](#api-reference)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Hardware

- **RAM**: Minimum 4GB (8GB+ recommended)
- **Disk Space**: 2GB free space
- **Processor**: Modern multi-core processor

### Software

- **OS**: Windows 10+, macOS 10.15+, or Linux
- **Python**: 3.8 or higher
- **pip**: Latest version
- **Git** (optional, for version control)

### Browser

- Chrome, Firefox, Safari, or Edge (latest version)

---

## Installation Steps

### Step 1: Verify Python Installation

```bash
python --version
# Should output: Python 3.8.x or higher

python -m pip --version
# Should show pip version
```

If Python is not installed:

- **Windows**: Download from https://www.python.org
- **macOS**: `brew install python3`
- **Linux**: `sudo apt install python3`

### Step 2: Navigate to Project Directory

```bash
# Windows
cd "C:\Users\YOUR_USER\Desktop\ml project\customer churn prediction"

# macOS/Linux
cd ~/Desktop/ml\ project/customer\ churn\ prediction
```

### Step 3: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Verify activation**: Your terminal should show `(venv)` prefix

### Step 4: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed**:

- Flask (web framework)
- scikit-learn (machine learning)
- XGBoost (gradient boosting)
- pandas (data processing)
- numpy (numerical computing)
- joblib (model serialization)
- matplotlib (visualization)

**Installation time**: 3-5 minutes

### Step 6: Verify Installation

```bash
python verify_setup.py
```

This will check:

- ✓ Python version
- ✓ All packages installed
- ✓ Project directories exist
- ✓ Required files present

---

## Running the Application

### Full Workflow (First Time)

#### 1. Generate Dataset

```bash
python generate_data.py
```

Output:

```
✓ Generated 5000 customer records
✓ Saved to data/churn_data.csv
✓ Churn rate: 26.8%
✓ Dataset shape: (5000, 16)

✓ Data generation complete!
```

#### 2. Train Machine Learning Model

```bash
python -m src.model
```

Output:

```
✓ Loaded 5000 records from data/churn_data.csv
✓ Preprocessed data: 15 features
✓ Train set: 4000, Test set: 1000
✓ Model trained successfully

==================================================
MODEL PERFORMANCE METRICS
==================================================
Accuracy:  80.5%
Precision: 67.2%
Recall:    59.4%
F1 Score:  63.1%
ROC-AUC:   87.2%
==================================================

MODEL COMPARISON
==================================================
              Model  Accuracy   ROC-AUC
       Random Forest      0.805    0.872
              XGBoost      0.798    0.865
 Logistic Regression      0.795    0.856
     Decision Tree       0.745    0.742
==================================================

✓ Model saved to models/
```

#### 3. Start Web Application

```bash
python run.py
```

Output:

```
============================================================
Customer Churn Prediction Web Application
============================================================
Starting Flask server...
Navigate to: http://127.0.0.1:5000
Demo login: admin / admin123
============================================================
 * Serving Flask app 'src.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

#### 4. Open Browser

- Go to: **http://127.0.0.1:5000**
- Login: `admin` / `admin123`

---

## Usage Guide

### Web Interface

#### 1. Login Page

- URL: `http://127.0.0.1:5000/login`
- Demo credentials:
  - Username: `admin`
  - Password: `admin123`

#### 2. Dashboard

- View key statistics
- Total predictions made
- Number of churn cases
- Average risk score
- High-risk customer count
- Recent predictions table

#### 3. Make Predictions

- Fill customer information form
- Fields include:
  - Age, Tenure, Charges
  - Internet Service Type
  - Contract Type
  - Services (Security, Support, TV, Movies)
  - Billing preferences
- Click "Make Prediction"
- View results with probability and risk level

#### 4. Prediction History

- View all past predictions
- See probability trends
- Risk level badges
- Customer details
- Sortable table

### API Usage

#### Base URL

```
http://127.0.0.1:5000
```

#### Make Prediction

```bash
POST /api/predict
Content-Type: application/json

{
  "age": 45,
  "tenure_months": 24,
  "monthly_charges": 75.5,
  "total_charges": 1800,
  "internet_service": "Fiber optic",
  "contract": "Month-to-month",
  "gender": "Male",
  "online_security": "Yes",
  "online_backup": "No",
  "device_protection": "No",
  "tech_support": "Yes",
  "streaming_tv": "Yes",
  "streaming_movies": "No",
  "paperless_billing": "Yes",
  "payment_method": "Electronic check",
  "customer_id": "CUST001"
}
```

Response:

```json
{
  "prediction": 1,
  "will_churn": true,
  "churn_probability": 0.75,
  "risk_level": "HIGH"
}
```

#### Get All Predictions

```bash
GET /api/predictions?limit=100
```

#### Get Statistics

```bash
GET /api/stats
```

Response:

```json
{
  "total_predictions": 42,
  "churned": 12,
  "not_churned": 30,
  "avg_churn_probability": 0.38,
  "high_risk_count": 8,
  "low_risk_count": 34
}
```

---

## Troubleshooting

### Issue 1: Module not found error

```
ModuleNotFoundError: No module named 'flask'
```

**Solution**:

```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: Dataset not found

```
FileNotFoundError: data/churn_data.csv
```

**Solution**:

```bash
# Generate the dataset
python generate_data.py
```

### Issue 3: Model files not found

```
FileNotFoundError: models/churn_model.pkl
```

**Solution**:

```bash
# Train the model
python -m src.model
```

### Issue 4: Port 5000 already in use

```
Address already in use
```

**Solution**:

```bash
# Option 1: Kill existing process
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Option 2: Use different port
# Edit run.py and change port 5000 to 8000 or another available port
```

### Issue 5: "No module named 'src'"

```
ModuleNotFoundError: No module named 'src'
```

**Solution**:

```bash
# Make sure you're in the project root directory
cd "customer churn prediction"

# Create __init__.py in src folder if missing
touch src/__init__.py  # macOS/Linux
# or
type nul > src/__init__.py  # Windows
```

### Issue 6: Virtual environment not activating

```bash
# Try alternative activation method
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# If that doesn't work, try command prompt
venv\Scripts\activate.bat
```

### Issue 7: CORS or connection issues

**Solution**:

- Clear browser cache (Ctrl+Shift+Delete)
- Try a different browser
- Disable browser extensions
- Check firewall settings

---

## Project Structure

```
customer_churn_prediction/
│
├── src/                          # Python package
│   ├── __init__.py
│   ├── model.py                  # ML model training & prediction
│   └── app.py                    # Flask web application
│
├── templates/                    # HTML pages
│   ├── base.html                 # Base template
│   ├── index.html                # Home page
│   ├── login.html                # Login page
│   ├── dashboard.html            # Dashboard
│   ├── predict.html              # Prediction form
│   └── history.html              # Prediction history
│
├── static/                       # Static files
│   ├── style.css                 # Styling
│   └── script.js                 # JavaScript utilities
│
├── data/                         # Data files
│   └── churn_data.csv           # Generated dataset
│
├── models/                       # Trained ML models
│   ├── churn_model.pkl          # Trained model
│   ├── scaler.pkl               # Feature scaler
│   ├── encoders.pkl             # Category encoders
│   └── features.pkl             # Feature list
│
├── documentation/               # Documentation
│   ├── README.md                # Full documentation
│   ├── API.md                   # API reference
│   ├── ARCHITECTURE.md          # System architecture
│   ├── DEPLOYMENT.md            # Deployment guide
│   ├── INTERVIEW_QA.md          # Interview questions
│   └── PROJECT_REPORT.md        # Project summary
│
├── generate_data.py             # Data generation script
├── run.py                        # Flask entry point
├── verify_setup.py              # Setup verification
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── QUICKSTART.md                # Quick start guide
└── SETUP.md                     # This file
```

---

## Performance Tips

### For Development

```bash
# Enable debug mode (already enabled in run.py)
# The server will auto-reload on file changes
```

### For Production

```bash
# Use Gunicorn server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app

# Or use Waitress on Windows
pip install waitress
waitress-serve --port=5000 src.app:app
```

---

## Next Steps

1. ✓ Complete Setup (you are here)
2. Make Predictions using the web interface
3. Test API with curl or Postman
4. Review code in `src/model.py` and `src/app.py`
5. Customize model parameters
6. Deploy to production (see `documentation/DEPLOYMENT.md`)

---

## Support & Documentation

- **Quick Start**: See `QUICKSTART.md`
- **Full Documentation**: See `documentation/README.md`
- **API Reference**: See `documentation/API.md`
- **Architecture**: See `documentation/ARCHITECTURE.md`
- **Deployment**: See `documentation/DEPLOYMENT.md`
- **Interview Prep**: See `documentation/INTERVIEW_QA.md`

---

## Version Information

- **Project Version**: 1.0.0
- **Last Updated**: June 18, 2026
- **Python Version**: 3.8+
- **Status**: ✅ Production Ready

---

**Congratulations! Your Customer Churn Prediction application is ready to use! 🎉**

For questions or issues, refer to the troubleshooting section above or check the documentation folder.
