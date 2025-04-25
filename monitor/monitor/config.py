import os


class Config:
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'mongodb')
    MONGODB_USER = os.getenv('MONGODB_USER', 'user')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'pass')
