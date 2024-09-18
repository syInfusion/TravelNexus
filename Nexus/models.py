from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from Nexus.db import mongo

class User:
    @staticmethod
    def create_user(username, email, password):
        hashed_password = generate_password_hash(password)
        user = {
            "username": username,
             "email": email,
             "password": hashed_password}
        mongo.db.users.insert_one(user)
        return user

    @staticmethod
    def find_user_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def check_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)