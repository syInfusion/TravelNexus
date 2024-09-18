import unittest
from flask_testing import TestCase
from Nexus import create_app
from Nexus.models import User
from Nexus.db import init_db

class DatabaseTestCase(TestCase):

    def create_app(self):
        app = create_app()
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        with self.app.app_context():
            init_db(self.app)

    def tearDown(self):
        with self.app.app_context():
            # Drop the test database
            User.drop_collection()

    def test_create_user(self):
        with self.app.app_context():
            user = User.create_user('testuser', 'test@example.com', 'password')
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'testuser')
            self.assertEqual(user.email, 'test@example.com')

    def test_find_user_by_email(self):
        with self.app.app_context():
            User.create_user('testuser', 'test@example.com', 'password')
            user = User.find_user_by_email('test@example.com')
            self.assertIsNotNone(user)
            self.assertEqual(user['email'], 'test@example.com')

    def test_check_password(self):
        with self.app.app_context():
            User.create_user('testuser', 'test@example.com', 'password')
            user = User.find_user_by_email('test@example.com')
            self.assertTrue(User.check_password(user['password'], 'password'))
            self.assertFalse(User.check_password(user['password'], 'wrongpassword'))

if __name__ == '__main__':
    unittest.main()