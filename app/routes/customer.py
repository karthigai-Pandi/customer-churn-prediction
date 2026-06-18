"""
Flask Routes: Customer Management
Handle customer CRUD operations
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from utils.database import DatabaseConnection
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')


def login_required(f):
    """Decorator for login required"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@customer_bp.route('/', methods=['GET'])
@login_required
def list_customers():
    """List all customers"""
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '')
        per_page = 20
        offset = (page - 1) * per_page
        
        # Base query
        query = "SELECT * FROM customers"
        params = []
        
        # Add search filter
        if search:
            query += " WHERE contract_id LIKE %s OR gender LIKE %s"
            search_param = f"%{search}%"
            params.extend([search_param, search_param])
        
        # Add pagination
        query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
        params.extend([per_page, offset])
        
        customers = DatabaseConnection.execute_query(query, params)
        
        # Get total count
        count_query = "SELECT COUNT(*) as count FROM customers"
        if search:
            count_query += " WHERE contract_id LIKE %s OR gender LIKE %s"
            total = DatabaseConnection.execute_query(
                count_query, (f"%{search}%", f"%{search}%"), fetch_one=True
            )['count']
        else:
            total = DatabaseConnection.execute_query(count_query, fetch_one=True)['count']
        
        total_pages = (total + per_page - 1) // per_page
        
        return render_template('customers.html',
                             customers=customers,
                             page=page,
                             total_pages=total_pages,
                             search=search,
                             total=total)
    
    except Exception as e:
        logger.error(f"Customer list error: {str(e)}")
        return render_template('error.html', error='Failed to load customers'), 500


@customer_bp.route('/<int:customer_id>', methods=['GET'])
@login_required
def view_customer(customer_id):
    """View customer details and predictions"""
    try:
        # Get customer
        customer_query = "SELECT * FROM customers WHERE customer_id = %s"
        customer = DatabaseConnection.execute_query(
            customer_query, (customer_id,), fetch_one=True
        )
        
        if not customer:
            return render_template('error.html', error='Customer not found'), 404
        
        # Get predictions for this customer
        pred_query = """
        SELECT prediction_id, churn_prediction, churn_probability, risk_level, 
               model_name, prediction_timestamp
        FROM predictions
        WHERE customer_id = %s
        ORDER BY prediction_timestamp DESC
        """
        
        predictions = DatabaseConnection.execute_query(pred_query, (customer_id,))
        
        return render_template('customer_detail.html',
                             customer=customer,
                             predictions=predictions)
    
    except Exception as e:
        logger.error(f"Customer detail error: {str(e)}")
        return render_template('error.html', error='Failed to load customer'), 500


@customer_bp.route('/', methods=['POST'])
@login_required
def create_customer():
    """Create new customer"""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Validation
        if not data.get('contract_id'):
            return jsonify({'status': 'error', 'message': 'Contract ID is required'}), 400
        
        # Check if customer already exists
        check_query = "SELECT customer_id FROM customers WHERE contract_id = %s"
        existing = DatabaseConnection.execute_query(
            check_query, (data.get('contract_id'),), fetch_one=True
        )
        
        if existing:
            return jsonify({'status': 'error', 'message': 'Customer already exists'}), 400
        
        # Insert customer
        customer_data = {
            'contract_id': data.get('contract_id'),
            'gender': data.get('gender', 'Unknown'),
            'age': int(data.get('age', 0)) if data.get('age') else 0,
            'tenure_months': int(data.get('tenure_months', 0)) if data.get('tenure_months') else 0,
            'phone_service': data.get('phone_service', 'No'),
            'internet_service': data.get('internet_service', 'DSL'),
            'online_security': data.get('online_security', 'No'),
            'online_backup': data.get('online_backup', 'No'),
            'device_protection': data.get('device_protection', 'No'),
            'tech_support': data.get('tech_support', 'No'),
            'streaming_tv': data.get('streaming_tv', 'No'),
            'streaming_movies': data.get('streaming_movies', 'No'),
            'contract': data.get('contract', 'Month-to-month'),
            'paperless_billing': data.get('paperless_billing', 'No'),
            'payment_method': data.get('payment_method', 'Electronic check'),
            'monthly_charges': float(data.get('monthly_charges', 0)) if data.get('monthly_charges') else 0,
            'total_charges': float(data.get('total_charges', 0)) if data.get('total_charges') else 0
        }
        
        customer_id = DatabaseConnection.insert_record('customers', customer_data)
        logger.info(f"New customer created: {customer_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Customer created successfully',
            'customer_id': customer_id
        }), 201
    
    except Exception as e:
        logger.error(f"Customer creation error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@customer_bp.route('/<int:customer_id>', methods=['PUT'])
@login_required
def update_customer(customer_id):
    """Update customer details"""
    try:
        data = request.get_json()
        
        # Prepare update data (only update provided fields)
        update_data = {}
        allowed_fields = ['gender', 'age', 'phone_service', 'internet_service',
                         'online_security', 'online_backup', 'device_protection',
                         'tech_support', 'streaming_tv', 'streaming_movies',
                         'contract', 'paperless_billing', 'payment_method',
                         'monthly_charges', 'total_charges']
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return jsonify({'status': 'error', 'message': 'No fields to update'}), 400
        
        # Update customer
        DatabaseConnection.update_record(
            'customers', update_data, 'customer_id = %s', [customer_id]
        )
        
        logger.info(f"Customer updated: {customer_id}")
        return jsonify({'status': 'success', 'message': 'Customer updated successfully'}), 200
    
    except Exception as e:
        logger.error(f"Customer update error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
