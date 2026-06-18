"""
Flask Routes: REST API
RESTful API endpoints for external integrations
"""
from flask import Blueprint, request, jsonify, session
from utils.database import DatabaseConnection
from utils.prediction import PredictionEngine, format_prediction_result, validate_input_data
from utils.export import ExportManager
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)


# API Key validation (simple implementation)
VALID_API_KEYS = {
    'demo-key-12345': {'name': 'Demo Key', 'permissions': ['predict', 'get_history']}
}


def require_api_key(f):
    """Decorator to require API key"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key or api_key not in VALID_API_KEYS:
            return jsonify({'status': 'error', 'message': 'Invalid or missing API key'}), 401
        
        request.api_key_info = VALID_API_KEYS[api_key]
        return f(*args, **kwargs)
    return decorated_function


# Initialize prediction engine
try:
    prediction_engine = PredictionEngine()
except:
    prediction_engine = None
    logger.warning("Prediction engine not available")


@api_bp.route('/predict', methods=['POST'])
@require_api_key
def api_predict():
    """
    API endpoint for making predictions
    
    Required headers:
        X-API-Key: Your API key
        
    Request body:
        {
            "contract_id": "CUST001",
            "tenure_months": 12,
            "monthly_charges": 65.5,
            "total_charges": 786.0,
            "internet_service": "Fiber optic",
            "phone_service": "Yes",
            ...other features
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['contract_id', 'tenure_months', 'monthly_charges', 'total_charges']
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
        
        # Format result
        result = format_prediction_result(
            prediction,
            contract_id=data.get('contract_id')
        )
        
        # Optionally save to database
        if data.get('save_prediction', False):
            try:
                prediction_data = {
                    'contract_id': data.get('contract_id'),
                    'churn_prediction': prediction['churn_prediction'],
                    'churn_probability': prediction['churn_probability'],
                    'risk_level': prediction['risk_level'],
                    'model_name': 'Random Forest',
                    'confidence_score': prediction['confidence_score']
                }
                
                prediction_id = DatabaseConnection.insert_record('predictions', prediction_data)
                result['prediction_id'] = prediction_id
            except Exception as e:
                logger.warning(f"Could not save prediction: {str(e)}")
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'data': result
        }), 200
    
    except Exception as e:
        logger.error(f"API prediction error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/predictions', methods=['GET'])
@require_api_key
def api_get_predictions():
    """
    API endpoint to get prediction history
    
    Query parameters:
        limit: Number of records to return (default: 20)
        offset: Pagination offset (default: 0)
        risk_level: Filter by risk level (High Risk, Low Risk)
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        risk_level = request.args.get('risk_level', None)
        
        # Build query
        query = "SELECT * FROM predictions WHERE 1=1"
        params = []
        
        if risk_level:
            query += " AND risk_level = %s"
            params.append(risk_level)
        
        query += " ORDER BY prediction_timestamp DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        predictions = DatabaseConnection.execute_query(query, params)
        
        # Get total count
        count_query = "SELECT COUNT(*) as count FROM predictions WHERE 1=1"
        if risk_level:
            count_query += " AND risk_level = %s"
            total = DatabaseConnection.execute_query(
                count_query, [risk_level] if risk_level else [], fetch_one=True
            )['count']
        else:
            total = DatabaseConnection.execute_query(count_query, fetch_one=True)['count']
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'total': total,
            'limit': limit,
            'offset': offset,
            'data': predictions
        }), 200
    
    except Exception as e:
        logger.error(f"API get predictions error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/customers', methods=['GET'])
@require_api_key
def api_get_customers():
    """
    API endpoint to get customers
    
    Query parameters:
        limit: Number of records (default: 20)
        offset: Pagination offset (default: 0)
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = "SELECT * FROM customers ORDER BY created_at DESC LIMIT %s OFFSET %s"
        customers = DatabaseConnection.execute_query(query, (limit, offset))
        
        count_query = "SELECT COUNT(*) as count FROM customers"
        total = DatabaseConnection.execute_query(count_query, fetch_one=True)['count']
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'total': total,
            'limit': limit,
            'offset': offset,
            'data': customers
        }), 200
    
    except Exception as e:
        logger.error(f"API get customers error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/export/predictions', methods=['GET'])
@require_api_key
def api_export_predictions():
    """
    API endpoint to export predictions
    
    Query parameters:
        format: 'csv' or 'pdf' (default: csv)
    """
    try:
        format_type = request.args.get('format', 'csv').lower()
        
        if format_type not in ['csv', 'pdf']:
            return jsonify({'status': 'error', 'message': 'Invalid format'}), 400
        
        # Get predictions
        query = "SELECT * FROM predictions ORDER BY prediction_timestamp DESC"
        predictions = DatabaseConnection.execute_query(query)
        
        if format_type == 'csv':
            csv_content = ExportManager.export_to_csv(predictions)
            return csv_content, 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': 'attachment; filename=predictions.csv'
            }
        else:
            pdf_content = ExportManager.export_to_pdf(
                predictions, 
                title="Churn Prediction Report"
            )
            return pdf_content, 200, {
                'Content-Type': 'application/pdf',
                'Content-Disposition': 'attachment; filename=predictions.pdf'
            }
    
    except Exception as e:
        logger.error(f"API export error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/health', methods=['GET'])
def api_health():
    """Health check endpoint"""
    try:
        # Test database connection
        DatabaseConnection.execute_query("SELECT 1", fetch_one=True)
        
        # Check if model is loaded
        model_status = 'loaded' if prediction_engine is not None else 'not_loaded'
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'model': model_status
        }), 200
    
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503
