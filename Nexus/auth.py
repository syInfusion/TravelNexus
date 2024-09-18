from flask import request, jsonify, current_app as app, Blueprint, flash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from Nexus.models import User
from Nexus.db import mongo
import os

auth = Blueprint('auth', __name__)


def get_request_data():
    if request.is_json:
        return request.get_json()
    else:
        return request.form.to_dict()


@auth.route("/register", methods=["POST"])
def register():
    try:
        data = get_request_data()
        if User.find_user_by_email(data['email']):
            return jsonify({"message": "User already exists"}), 400
        user = User.create_user(
            data['username'], 
            data['email'], 
            data['password'])
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@auth.route("/login", methods=["POST"])
def login():
    try:
        data = get_request_data()
        user = User.find_user_by_email(data['email'])
        if not user or not User.check_password(user['password'], data['password']):
            return jsonify({"message": "Invalid credentials"}), 401
        access_token = create_access_token(identity=user['email'])
        flash('Logged in successfully', category='success')
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500