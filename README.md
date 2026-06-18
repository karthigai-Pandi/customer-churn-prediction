# Customer Churn Prediction Web Application

A complete end-to-end machine learning web application for predicting customer churn using advanced algorithms and a professional web interface.

## 🎯 Features

- **Machine Learning Models**: Logistic Regression, Decision Tree, Random Forest, XGBoost
- **Advanced Analytics**: EDA with interactive visualizations
- **RESTful API**: Complete REST API for integrations
- **User Management**: Secure login and authentication
- **Customer Management**: CRUD operations for customers
- **Prediction History**: Track all predictions with timestamps
- **Risk Assessment**: High Risk/Low Risk classification
- **Export Reports**: PDF and CSV export functionality
- **Responsive Design**: Mobile-friendly Bootstrap UI
- **MySQL Database**: Persistent data storage

## 📋 Requirements

- Python 3.8+
- MySQL 5.7+
- Flask 2.3+
- Scikit-learn, XGBoost
- Bootstrap 5
- Modern web browser

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd customer_churn_prediction

# Create Python environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate
# or (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Login to MySQL
mysql -u root -p

# Run schema
SOURCE database/schema.sql;

# Run sample data
SOURCE database/sample_data.sql;

# Exit MySQL
exit;
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# MYSQL_HOST=localhost
# MYSQL_USER=root
# MYSQL_PASSWORD=your_password
# MYSQL_DB=customer_churn_db
# SECRET_KEY=your_secret_key
```

### 4. Download Dataset

Download the Telco Customer Churn dataset from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn):

```bash
# Create data directory
mkdir data

# Place the CSV file
# data/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

Or use Kaggle CLI:

```bash
kaggle datasets download -d blastchar/telco-customer-churn
unzip telco-customer-churn.zip -d data/
```

### 5. Train ML Models

```bash
cd ml_pipeline
python train_pipeline.py
```

This will:

- Load and preprocess the dataset
- Train all models
- Generate EDA report
- Select best model
- Save trained models

### 6. Run Application

```bash
# From project root
python run.py
```

Visit: `http://localhost:5000`

**Default Credentials:**

- Username: `admin`
- Password: `admin123`

## 📁 Project Structure

```
customer_churn_prediction/
├── app/                           # Flask application
│   ├── routes/                    # Route blueprints
│   │   ├── auth.py               # Authentication routes
│   │   ├── dashboard.py          # Dashboard routes
│   │   ├── prediction.py         # Prediction routes
│   │   ├── customer.py           # Customer management
│   │   ├── analytics.py          # Analytics routes
│   │   └── api.py                # REST API routes
│   ├── static/                    # Static files
│   │   ├── css/
│   │   │   └── style.css         # Main stylesheet
│   │   └── js/
│   │       └── main.js           # JavaScript utilities
│   ├── templates/                 # HTML templates
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── predict.html
│   │   ├── prediction_history.html
│   │   ├── customers.html
│   │   ├── analytics.html
│   │   └── navbar.html
│   └── __init__.py               # Flask app factory
├── ml_pipeline/                   # Machine Learning
│   ├── data_processor.py         # Data preprocessing
│   ├── model_trainer.py          # Model training
│   ├── eda.py                    # EDA and visualization
│   └── train_pipeline.py         # Main training script
├── utils/                         # Utility modules
│   ├── database.py               # Database operations
│   ├── prediction.py             # Prediction engine
│   └── export.py                 # PDF/CSV export
├── config/                        # Configuration
│   └── config.py                 # App configuration
├── database/                      # Database files
│   ├── schema.sql                # Database schema
│   └── sample_data.sql           # Sample data
├── models/                        # Trained models
│   ├── best_model.pkl
│   ├── scaler.pkl
│   ├── encoder.pkl
│   └── feature_columns.pkl
├── documentation/                 # Documentation
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

## 🔧 Configuration

### Environment Variables (.env)

```
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=your_secret_key_change_in_production
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=customer_churn_db
DEBUG=True
```

## 📊 Machine Learning Pipeline

### Data Preprocessing

1. Load CSV data
2. Handle missing values
3. Remove duplicates
4. Identify data types
5. Encode categorical features
6. Scale numerical features

### Models Trained

1. **Logistic Regression** - Baseline model
2. **Decision Tree** - Rule-based model
3. **Random Forest** - Ensemble model (Selected)
4. **XGBoost** - Gradient boosting model

### Model Selection

Models are evaluated on:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC (Primary metric)

**Best Model**: Random Forest with highest ROC-AUC score

### Performance Metrics

Metrics stored in `models/training_report.txt` and database.

## 🌐 REST API Endpoints

### Authentication

```
POST   /api/predict              - Make prediction
GET    /api/predictions          - Get predictions
GET    /api/customers            - Get customers
GET    /api/export/predictions   - Export predictions
GET    /api/health               - Health check
```

### Headers Required

```
X-API-Key: demo-key-12345
Content-Type: application/json
```

### Example: Make Prediction

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
    "online_security": "No",
    "contract": "Month-to-month"
  }'
```

## 🎨 Frontend Features

### Pages

1. **Login/Register** - User authentication
2. **Dashboard** - Overview and recent predictions
3. **Prediction** - Interactive form for new predictions
4. **History** - Prediction history with pagination
5. **Customers** - Customer management interface
6. **Analytics** - Charts and model performance

### UI Technologies

- Bootstrap 5 - Responsive grid system
- Font Awesome - Icons
- Chart.js - Data visualization
- Custom CSS - Modern styling

## 🗄️ Database Schema

### Tables

- **users** - User accounts
- **customers** - Customer information
- **predictions** - Prediction records
- **model_performance** - Model metrics
- **audit_log** - Activity logging
- **statistics** - System statistics

## 🔐 Security Features

- Password hashing with Werkzeug
- Session management
- API key authentication
- Input validation
- SQL injection prevention
- CORS support

## 📈 Performance Metrics

Default model (Random Forest) performance:

- **Accuracy**: ~80.5%
- **Precision**: ~67.2%
- **Recall**: ~59.4%
- **F1 Score**: ~63.1%
- **ROC-AUC**: ~87.2%

## 🚢 Deployment

### Render Deployment

1. **Create Render Account**
   - Sign up at render.com

2. **Create MySQL Database**
   - Create new MySQL database
   - Copy connection string

3. **Update .env**

   ```
   MYSQL_HOST=your-render-db.c.db.onrender.com
   MYSQL_USER=username
   MYSQL_PASSWORD=password
   MYSQL_DB=database_name
   ```

4. **Push to GitHub**

   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

5. **Create Web Service on Render**
   - Connect GitHub repository
   - Set Python environment
   - Add environment variables from .env
   - Deploy

6. **Run Migrations**
   - Connect via SSH
   - Run database schema
   - Upload sample data

## 🐛 Troubleshooting

### Database Connection Error

```
Error: MySQL connection refused
Solution:
1. Ensure MySQL is running
2. Check credentials in .env
3. Verify database exists
```

### Models Not Found

```
Error: Model files not found
Solution:
1. Run ml_pipeline/train_pipeline.py
2. Check models/ directory
3. Verify joblib installation
```

### Static Files Not Loading

```
Error: CSS/JS not loading
Solution:
1. Check static folder exists
2. Restart Flask application
3. Clear browser cache
```

## 📚 Documentation Files

- `API.md` - REST API documentation
- `ARCHITECTURE.md` - System architecture
- `DEPLOYMENT.md` - Deployment guide
- `INTERVIEW_QA.md` - Interview questions
- `PROJECT_REPORT.md` - Detailed project report

## 👥 Default Test Accounts

| Username | Password   | Role          |
| -------- | ---------- | ------------- |
| admin    | admin123   | Administrator |
| analyst1 | analyst123 | Analyst       |
| manager1 | manager123 | Manager       |

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🤝 Support

For issues or questions:

1. Check documentation files
2. Review error logs in `/logs`
3. Verify database connection
4. Check Flask debug output

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn Guide](https://scikit-learn.org/)
- [XGBoost Docs](https://xgboost.readthedocs.io/)
- [Bootstrap 5](https://getbootstrap.com/)
- [MySQL](https://dev.mysql.com/doc/)

---

**Last Updated**: June 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
