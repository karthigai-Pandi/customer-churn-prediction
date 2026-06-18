"""
Flask Routes: Authentication
Handles user login, logout, and registration
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from utils.database import DatabaseConnection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            if request.is_json:
                return jsonify({'status': 'error', 'message': 'Username and password required'}), 400
            return redirect(url_for('auth.login'))
        
        try:
            # Check user credentials
            query = "SELECT user_id, username, password_hash, full_name FROM users WHERE username = %s"
            user = DatabaseConnection.execute_query(query, (username,), fetch_one=True)
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                session['full_name'] = user['full_name']
                logger.info(f"User {username} logged in successfully")
                
                if request.is_json:
                    return jsonify({'status': 'success', 'message': 'Login successful'}), 200
                return redirect(url_for('dashboard.index'))
            else:
                logger.warning(f"Failed login attempt for user {username}")
                if request.is_json:
                    return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
                return render_template('login.html', error='Invalid username or password')
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            if request.is_json:
                return jsonify({'status': 'error', 'message': 'Login failed'}), 500
            return render_template('login.html', error='An error occurred during login')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        
        # Validation
        if not username or not email or not password:
            if request.is_json:
                return jsonify({'status': 'error', 'message': 'All fields required'}), 400
            return render_template('register.html', error='All fields are required')
        
        if len(password) < 6:
            if request.is_json:
                return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters'}), 400
            return render_template('register.html', error='Password must be at least 6 characters')
        
        try:
            # Check if user exists
            query = "SELECT user_id FROM users WHERE username = %s OR email = %s"
            existing_user = DatabaseConnection.execute_query(query, (username, email), fetch_one=True)
            
            if existing_user:
                if request.is_json:
                    return jsonify({'status': 'error', 'message': 'Username or email already exists'}), 400
                return render_template('register.html', error='Username or email already exists')
            
            # Create new user
            password_hash = generate_password_hash(password)
            user_data = {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'full_name': full_name
            }
            
            user_id = DatabaseConnection.insert_record('users', user_data)
            logger.info(f"New user registered: {username}")
            
            if request.is_json:
                return jsonify({'status': 'success', 'message': 'Registration successful'}), 201
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            if request.is_json:
                return jsonify({'status': 'error', 'message': 'Registration failed'}), 500
            return render_template('register.html', error='An error occurred during registration')
    
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    logger.info("User logged out")
    return redirect(url_for('auth.login'))
