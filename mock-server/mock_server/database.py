from pymongo import MongoClient
from .config import Config

class Database:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._client = MongoClient(Config.MONGODB_URI)
            self._db = self._client[Config.MONGODB_DB_NAME]

    @property
    def db(self):
        return self._db

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None 