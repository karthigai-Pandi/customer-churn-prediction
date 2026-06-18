"""
Flask Web Application for Customer Churn Prediction
Provides REST API and web interface for churn predictions
"""

from flask import Flask, render_template, request, jsonify, session
from functools import wraps
import os
import joblib
import json
import numpy as np
from datetime import datetime, timedelta
from src.model import ChurnPredictor

# Get the project root directory (parent of src/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(project_root, 'templates')
static_dir = os.path.join(project_root, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize predictor
predictor = ChurnPredictor()
try:
    predictor.load_model()
    print("✓ Model loaded successfully")
except:
    print("⚠ Model not found. Please run: python generate_data.py && python -m src.model")

# Store predictions in memory (use database in production)
predictions_history = []

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Simple authentication (use proper auth in production)
        if data.get('username') == 'admin' and data.get('password') == 'admin123':
            session['user'] = data['username']
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=24)
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return jsonify({'success': True})

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    stats = {
        'total_predictions': len(predictions_history),
        'churn_cases': sum(1 for p in predictions_history if p['will_churn']),
        'avg_risk': np.mean([p['churn_probability'] for p in predictions_history]) if predictions_history else 0,
        'high_risk_count': sum(1 for p in predictions_history if p['risk_level'] == 'HIGH')
    }
    return render_template('dashboard.html', stats=stats, predictions=predictions_history[-10:])

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Prediction page and API endpoint"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Make prediction
            result = predictor.predict(data)
            
            # Store in history
            prediction_record = {
                'timestamp': datetime.now().isoformat(),
                'customer_id': data.get('customer_id', 'N/A'),
                'input': data,
                **result
            }
            predictions_history.append(prediction_record)
            
            return jsonify(result)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('predict.html')

@app.route('/history')
@login_required
def history():
    """Prediction history page"""
    return render_template('history.html', predictions=predictions_history)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """REST API for predictions"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result = predictor.predict(data)
        
        # Store in history
        prediction_record = {
            'timestamp': datetime.now().isoformat(),
            **result,
            'input': data
        }
        predictions_history.append(prediction_record)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """Get prediction history via API"""
    limit = request.args.get('limit', 100, type=int)
    return jsonify(predictions_history[-limit:])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics via API"""
    stats = {
        'total_predictions': len(predictions_history),
        'churned': sum(1 for p in predictions_history if p['will_churn']),
        'not_churned': sum(1 for p in predictions_history if not p['will_churn']),
        'avg_churn_probability': np.mean([p['churn_probability'] for p in predictions_history]) if predictions_history else 0,
        'high_risk_count': sum(1 for p in predictions_history if p['risk_level'] == 'HIGH'),
        'low_risk_count': sum(1 for p in predictions_history if p['risk_level'] == 'LOW'),
    }
    return jsonify(stats)

@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
