import os

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/')
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'mongodb')
    MONGODB_USER = os.environ['MONGODB_USER']
    MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']

    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', '1') 