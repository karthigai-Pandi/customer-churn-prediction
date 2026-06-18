"""
Flask Routes: Dashboard
Main dashboard view
"""
from flask import Blueprint, render_template, session, redirect, url_for
from utils.database import DatabaseConnection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def login_required(f):
    """Decorator for login required"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard main page"""
    try:
        user_id = session.get('user_id')
        
        # Get statistics
        stats_query = """
        SELECT 
            COUNT(DISTINCT customer_id) as total_customers,
            COUNT(DISTINCT prediction_id) as total_predictions,
            SUM(CASE WHEN churn_prediction = 1 THEN 1 ELSE 0 END) as high_risk_count,
            AVG(churn_probability) as avg_churn_probability
        FROM predictions WHERE user_id = %s
        """
        
        stats = DatabaseConnection.execute_query(stats_query, (user_id,), fetch_one=True)
        
        # Get recent predictions
        recent_query = """
        SELECT p.prediction_id, p.contract_id, p.churn_prediction, 
               p.churn_probability, p.risk_level, p.prediction_timestamp
        FROM predictions p
        WHERE p.user_id = %s
        ORDER BY p.prediction_timestamp DESC
        LIMIT 10
        """
        
        recent_predictions = DatabaseConnection.execute_query(recent_query, (user_id,))
        
        return render_template('dashboard.html', 
                             stats=stats, 
                             recent_predictions=recent_predictions)
    
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        return render_template('error.html', error='Failed to load dashboard'), 500
