from flask import request, jsonify, Blueprint, flash, url_for
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from Nexus.models import User
from Nexus.db import mongo
import re

# Create a Blueprint named 'auth' to organize the authentication routes
auth = Blueprint('auth', __name__)

# Function to get request data, whether it's JSON or form data
def get_request_data():
    if request.is_json:
        return request.get_json()
    else:
        return request.form.to_dict()

# Function to validate email format using a regular expression
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

# Function to validate registration data
def validate_registration_data(data):
    if 'username' not in data or not data['username'].strip():
        return "Username is required"
    if 'email' not in data or not data['email'].strip():
        return "Email is required"
    if not is_valid_email(data['email']):
        return "Email is not valid"
    if 'password' not in data or not data['password'].strip():
        return "Password is required"
    return None

# Function to validate login data
def validate_login_data(data):
    if 'email' not in data or not data['email'].strip():
        return "Email is required"
    if not is_valid_email(data['email']):
        return "Email is not valid"
    if 'password' not in data or not data['password'].strip():
        return "Password is required"
    return None

# Route to handle user registration
@auth.route("/register", methods=["POST"])
def register():
    try:
        data = get_request_data()
        validation_error = validate_registration_data(data)
        if validation_error:
            return jsonify({"message": validation_error}), 400

        if User.find_user_by_email(data['email']):
            return jsonify({"message": "User already exists"}), 400

        user = User.create_user(data['username'], data['email'], data['password'])
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Route to handle user login
@auth.route("/login", methods=["POST"])
def login():
    try:
        data = get_request_data()
        validation_error = validate_login_data(data)
        if validation_error:
            return jsonify({"message": validation_error}), 400

        user = User.find_user_by_email(data['email'])
        if not user or not User.check_password(user['password'], data['password']):
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = create_access_token(identity=user['email'])
        flash('Logged in successfully', category='success')
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
