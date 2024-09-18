import unittest
from flask import current_app
from flask_testing import TestCase
from Nexus import create_app
from Nexus.models import User
from Nexus.db import init_db

class AuthTestCase(TestCase):
    """
    AuthTestCase is a test case for testing authentication-related functionalities.
    Methods:
        create_app():
            Creates and configures the Flask application for testing.
        setUp():
            Sets up the test environment, including initializing the database and adding a test user.
        tearDown():
            Cleans up the test environment by dropping the test database.
        test_register():
            Tests the user registration endpoint to ensure a new user can be registered successfully.
        test_register_existing_user():
            Tests the user registration endpoint to ensure registering an existing user returns an appropriate error.
        test_login():
            Tests the login endpoint to ensure a user can log in with valid credentials.
        test_login_invalid_credentials():
            Tests the login endpoint to ensure logging in with invalid credentials returns an appropriate error.
    """

    def create_app(self):
        app = create_app()
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        with self.app.app_context():
            init_db(self.app)
            # Add a test user
            User.create_user('testuser', 'test@example.com', 'password')

    def tearDown(self):
        with self.app.app_context():
            # Drop the test database
            User.drop_collection()

    def test_register(self):
        response = self.client.post('/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.json['message'])

    def test_register_existing_user(self):
        response = self.client.post('/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('User already exists', response.json['message'])

    def test_login(self):
        response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_login_invalid_credentials(self):
        response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.json['message'])

if __name__ == '__main__':
    unittest.main()