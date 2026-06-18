"""
Flask Routes: Prediction
Handle customer churn predictions
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from utils.database import DatabaseConnection
from utils.prediction import PredictionEngine, format_prediction_result, validate_input_data
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

prediction_bp = Blueprint('prediction', __name__, url_prefix='/predict')


def login_required(f):
    """Decorator for login required"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# Initialize prediction engine (load once at startup)
try:
    prediction_engine = PredictionEngine()
except:
    prediction_engine = None
    logger.warning("Prediction engine not available. Models may not be trained.")


@prediction_bp.route('/', methods=['GET', 'POST'])
@login_required
def predict_page():
    """Prediction form page"""
    if request.method == 'POST':
        try:
            # Get form data
            data = request.get_json() if request.is_json else request.form.to_dict()
            
            # Required fields for prediction
            required_fields = ['contract_id', 'tenure_months', 'monthly_charges', 
                             'total_charges', 'internet_service']
            
            is_valid, error_msg = validate_input_data(data, required_fields)
            if not is_valid:
                return jsonify({'status': 'error', 'message': error_msg}), 400
            
            # Prepare input for model
            input_data = {
                'tenure_months': float(data.get('tenure_months', 0)),
                'monthly_charges': float(data.get('monthly_charges', 0)),
                'total_charges': float(data.get('total_charges', 0)),
                'age': int(data.get('age', 40)),
                'internet_service': data.get('internet_service', 'DSL'),
                'phone_service': data.get('phone_service', 'No'),
                'online_security': data.get('online_security', 'No'),
                'online_backup': data.get('online_backup', 'No'),
                'device_protection': data.get('device_protection', 'No'),
                'tech_support': data.get('tech_support', 'No'),
                'streaming_tv': data.get('streaming_tv', 'No'),
                'streaming_movies': data.get('streaming_movies', 'No'),
                'contract': data.get('contract', 'Month-to-month'),
                'paperless_billing': data.get('paperless_billing', 'No'),
                'payment_method': data.get('payment_method', 'Electronic check')
            }
            
            # Make prediction
            if prediction_engine is None:
                return jsonify({'status': 'error', 'message': 'Prediction model not available'}), 503
            
            prediction = prediction_engine.predict(input_data)
            
            # Save to database
            user_id = session.get('user_id')
            prediction_data = {
                'user_id': user_id,
                'contract_id': data.get('contract_id'),
                'churn_prediction': prediction['churn_prediction'],
                'churn_probability': prediction['churn_probability'],
                'risk_level': prediction['risk_level'],
                'model_name': 'Random Forest',
                'confidence_score': prediction['confidence_score'],
                'notes': data.get('notes', '')
            }
            
            prediction_id = DatabaseConnection.insert_record('predictions', prediction_data)
            
            result = format_prediction_result(prediction, 
                                            contract_id=data.get('contract_id'))
            result['prediction_id'] = prediction_id
            
            logger.info(f"Prediction made and saved: {prediction_id}")
            
            if request.is_json:
                return jsonify({'status': 'success', 'data': result}), 201
            return render_template('prediction_result.html', result=result)
        
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            if request.is_json:
                return jsonify({'status': 'error', 'message': str(e)}), 500
            return render_template('error.html', error='Prediction failed'), 500
    
    return render_template('predict.html')


@prediction_bp.route('/history')
@login_required
def history():
    """View prediction history"""
    try:
        user_id = session.get('user_id')
        page = request.args.get('page', 1, type=int)
        per_page = 20
        offset = (page - 1) * per_page
        
        # Get predictions with pagination
        query = """
        SELECT prediction_id, contract_id, churn_prediction, churn_probability, 
               risk_level, model_name, prediction_timestamp
        FROM predictions
        WHERE user_id = %s
        ORDER BY prediction_timestamp DESC
        LIMIT %s OFFSET %s
        """
        
        predictions = DatabaseConnection.execute_query(
            query, (user_id, per_page, offset)
        )
        
        # Get total count
        count_query = "SELECT COUNT(*) as count FROM predictions WHERE user_id = %s"
        total = DatabaseConnection.execute_query(count_query, (user_id,), fetch_one=True)['count']
        total_pages = (total + per_page - 1) // per_page
        
        return render_template('prediction_history.html', 
                             predictions=predictions,
                             page=page,
                             total_pages=total_pages,
                             total=total)
    
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        return render_template('error.html', error='Failed to load history'), 500
