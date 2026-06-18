# Quick Start Guide - Customer Churn Prediction

Get the application running in 5 minutes.

## Prerequisites

- Python 3.8+ installed
- pip package manager
- Windows, Mac, or Linux OS

## 1. Clone/Extract Project

```bash
# Navigate to project folder
cd "customer churn prediction"
```

## 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Expected output**: `(venv)` prefix in your terminal

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Packages installed**:

- Flask, scikit-learn, XGBoost, pandas, numpy, joblib, matplotlib

## 4. Generate Synthetic Dataset

```bash
python generate_data.py
```

**Output**: Creates `data/churn_data.csv` with 5,000 customer records

## 5. Train Machine Learning Model

```bash
python -m src.model
```

**What happens**:

- Loads the CSV dataset
- Preprocesses data
- Trains 4 different ML models
- Selects best model (Random Forest)
- Saves trained model to `models/` folder

**Expected output**:

```
✓ Loaded 5000 records from data/churn_data.csv
✓ Preprocessed data: 15 features
✓ Train set: 4000, Test set: 1000

==================================================
MODEL PERFORMANCE METRICS
==================================================
Accuracy:  80.5%
Precision: 67.2%
Recall:    59.4%
F1 Score:  63.1%
ROC-AUC:   87.2%
==================================================
```

## 6. Start Flask Web Application

```bash
python run.py
```

**Expected output**:

```
============================================================
Customer Churn Prediction Web Application
============================================================
Starting Flask server...
Navigate to: http://127.0.0.1:5000
Demo login: admin / admin123
============================================================
```

## 7. Open Web Browser

1. Go to: **http://127.0.0.1:5000**
2. Login with:
   - Username: `admin`
   - Password: `admin123`

## 8. Use the Application

### Dashboard

- View prediction statistics
- See recent predictions
- Monitor churn cases

### Make Prediction

- Fill in customer information form
- Click "Make Prediction"
- View result with churn probability and risk level

### View History

- See all past predictions
- View prediction details
- Track churn probability trends

### API Usage

Make predictions programmatically:

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## Troubleshooting

### Issue: "Module not found" error

**Solution**: Make sure virtual environment is activated (see step 2)

### Issue: "No such file or directory: data/churn_data.csv"

**Solution**: Run `python generate_data.py` first (see step 4)

### Issue: "Model files not found"

**Solution**: Run `python -m src.model` to train the model (see step 5)

### Issue: Port 5000 already in use

**Solution**:

```bash
# Edit run.py and change port 5000 to another number like 8000
# Or kill existing process:
# Windows: netstat -ano | findstr :5000
#         taskkill /PID <PID> /F
```

### Issue: "No module named 'src'"

**Solution**: Make sure you're in the project root directory before running commands

## Project Structure

```
customer_churn_prediction/
├── src/
│   ├── model.py          # ML model training & prediction
│   ├── app.py            # Flask web application
│   └── __init__.py       # Package initialization
├── templates/            # HTML pages
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── predict.html
│   └── history.html
├── static/               # CSS & JavaScript
│   ├── style.css
│   └── script.js
├── data/                 # Dataset
│   └── churn_data.csv
├── models/               # Trained ML models
├── generate_data.py      # Data generation script
├── run.py                # Flask entry point
└── requirements.txt      # Python dependencies
```

## Next Steps

1. **Explore the Code**: Read the comments in `src/model.py` and `src/app.py`
2. **Make Predictions**: Use the web interface to predict churn
3. **Test API**: Use curl or Postman to test REST API
4. **Deploy**: Follow `documentation/DEPLOYMENT.md` for production deployment
5. **Customize**: Modify the model or features for your needs

## Key Features

✓ Real-time churn predictions  
✓ Probability and risk assessment  
✓ Prediction history tracking  
✓ RESTful API for integration  
✓ Professional web interface  
✓ Machine learning pipeline  
✓ Model comparison & evaluation

## Documentation

- **README.md** - Full project documentation
- **documentation/API.md** - REST API reference
- **documentation/ARCHITECTURE.md** - System design
- **documentation/DEPLOYMENT.md** - Production deployment
- **documentation/INTERVIEW_QA.md** - Interview preparation

## Support

For issues or questions:

1. Check the documentation folder
2. Review the code comments
3. Check troubleshooting section above

---

**Version**: 1.0.0  
**Last Updated**: June 18, 2026  
**Status**: ✅ Ready to Use
