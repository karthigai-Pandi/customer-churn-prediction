"""
Flask Application: Main App Initialization
Creates and configures the Flask application
"""
from flask import Flask, render_template, request, jsonify, send_file, session
from functools import wraps
import logging
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Create and configure Flask application
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    from config.config import get_config
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.prediction import prediction_bp
    from app.routes.customer import customer_bp
    from app.routes.analytics import analytics_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors"""
        logger.error(f"Server error: {str(error)}")
        return render_template('500.html'), 500
    
    @app.before_request
    def before_request():
        """Execute before each request"""
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=24)
    
    logger.info(f"Flask app created with config: {config_name}")
    return app


# Decorator for login required
def login_required(f):
    """
    Decorator to require login for a route
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return {'status': 'error', 'message': 'Login required'}, 401
        return f(*args, **kwargs)
    return decorated_function
