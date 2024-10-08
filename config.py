import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    TESTING = False

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MONGO_URI = "mongodb://localhost:27017/testdb"