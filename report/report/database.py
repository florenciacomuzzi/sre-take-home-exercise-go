from pymongo import MongoClient
from report.config import Config


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
            # Construct the MongoDB URI with authentication
            uri = f"mongodb://{Config.MONGODB_USER}:{Config.MONGODB_PASSWORD}@{Config.MONGODB_URI.split('://')[1]}"
            self._client = MongoClient(uri)
            self._db = self._client[Config.MONGODB_DB_NAME]

    @property
    def db(self):
        return self._db

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    def aggregate(self, collection_name: str, pipeline: list) -> list:
        """
        Run a MongoDB aggregation pipeline on the specified collection.

        Args:
            collection_name (str): The name of the collection to run the aggregation on
            pipeline (list): List of pipeline stages to execute

        Returns:
            list: The results of the aggregation pipeline
        """
        collection = self._db[collection_name]
        return list(collection.aggregate(pipeline))
