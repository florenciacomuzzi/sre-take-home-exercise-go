import os

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/')
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'mongodb')
    MONGODB_USER = os.getenv('MONGODB_USER', 'admin')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'password')

    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', '1') 