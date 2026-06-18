"""
Flask Routes: Analytics and Reporting
Analytics dashboard and model performance visualization
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from utils.database import DatabaseConnection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')


def login_required(f):
    """Decorator for login required"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@analytics_bp.route('/')
@login_required
def dashboard():
    """Analytics dashboard"""
    try:
        user_id = session.get('user_id')
        
        # Overall statistics
        stats_query = """
        SELECT 
            COUNT(DISTINCT customer_id) as total_customers,
            COUNT(*) as total_predictions,
            SUM(CASE WHEN churn_prediction = 1 THEN 1 ELSE 0 END) as churned_count,
            ROUND(AVG(churn_probability), 4) as avg_churn_prob,
            SUM(CASE WHEN risk_level = 'High Risk' THEN 1 ELSE 0 END) as high_risk_count
        FROM predictions
        WHERE user_id = %s
        """
        stats = DatabaseConnection.execute_query(stats_query, (user_id,), fetch_one=True)
        
        # Risk level distribution
        risk_query = """
        SELECT risk_level, COUNT(*) as count
        FROM predictions
        WHERE user_id = %s
        GROUP BY risk_level
        """
        risk_distribution = DatabaseConnection.execute_query(risk_query, (user_id,))
        
        # Churn distribution
        churn_query = """
        SELECT 
            CASE WHEN churn_prediction = 1 THEN 'Churned' ELSE 'Retained' END as status,
            COUNT(*) as count
        FROM predictions
        WHERE user_id = %s
        GROUP BY churn_prediction
        """
        churn_distribution = DatabaseConnection.execute_query(churn_query, (user_id,))
        
        # Model performance
        model_query = """
        SELECT model_name, accuracy, precision, recall, f1_score, roc_auc
        FROM model_performance
        ORDER BY training_date DESC
        """
        model_performance = DatabaseConnection.execute_query(model_query)
        
        return render_template('analytics.html',
                             stats=stats,
                             risk_distribution=risk_distribution,
                             churn_distribution=churn_distribution,
                             model_performance=model_performance)
    
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        return render_template('error.html', error='Failed to load analytics'), 500


@analytics_bp.route('/model-performance')
@login_required
def model_performance():
    """Model performance details"""
    try:
        query = """
        SELECT model_name, accuracy, precision, recall, f1_score, roc_auc, 
               training_date, data_size, is_best_model
        FROM model_performance
        ORDER BY training_date DESC
        """
        
        models = DatabaseConnection.execute_query(query)
        
        return render_template('model_performance.html', models=models)
    
    except Exception as e:
        logger.error(f"Model performance error: {str(e)}")
        return render_template('error.html', error='Failed to load model performance'), 500


@analytics_bp.route('/api/risk-distribution')
@login_required
def api_risk_distribution():
    """API endpoint for risk distribution data"""
    try:
        user_id = session.get('user_id')
        
        query = """
        SELECT risk_level, COUNT(*) as count
        FROM predictions
        WHERE user_id = %s
        GROUP BY risk_level
        """
        
        data = DatabaseConnection.execute_query(query, (user_id,))
        
        return jsonify({
            'status': 'success',
            'data': data
        }), 200
    
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@analytics_bp.route('/api/churn-distribution')
@login_required
def api_churn_distribution():
    """API endpoint for churn distribution data"""
    try:
        user_id = session.get('user_id')
        
        query = """
        SELECT 
            CASE WHEN churn_prediction = 1 THEN 'Churned' ELSE 'Retained' END as status,
            COUNT(*) as count
        FROM predictions
        WHERE user_id = %s
        GROUP BY churn_prediction
        """
        
        data = DatabaseConnection.execute_query(query, (user_id,))
        
        return jsonify({
            'status': 'success',
            'data': data
        }), 200
    
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
