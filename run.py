"""
Flask Application: Main Run File
Entry point for the Flask application
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import app


if __name__ == '__main__':
    
    # Run development server
    debug = os.getenv('DEBUG', 'True') == 'True'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"\n{'='*80}")
    print("Customer Churn Prediction Web Application")
    print(f"{'='*80}")
    print(f"Running on: http://{host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"{'='*80}\n")
    
    app.run(host=host, port=port, debug=debug)
