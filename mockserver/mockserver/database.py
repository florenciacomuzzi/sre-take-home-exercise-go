from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from mockserver.config import Config
from typing import List, Dict, Any
from datetime import datetime


class Database:
    _instance = None
    _client = None
    _db = None
    _buffer = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            # Construct the MongoDB URI with authentication
            uri = (f"mongodb://"
                   f"{Config.MONGODB_USER}:{Config.MONGODB_PASSWORD}@"
                   f"{Config.MONGODB_URI.split('://')[1]}")
            self._client = MongoClient(uri)
            self._db = self._client[Config.MONGODB_DB_NAME]
        # Number of records to buffer before bulk insert
        self._buffer_size = int(Config.MONGODB_BUFFER_SIZE)

    @property
    def db(self):
        return self._db

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    def insert_record(self, collection_name: str, record: Dict[str, Any]) -> None:
        """
        Insert a single record into the specified collection.
        Uses buffering for better performance.

        Args:
            collection_name (str): Name of the collection
            record (Dict[str, Any]): Record to insert
        """
        # Remove _id field if it exists to let MongoDB generate a new one
        if '_id' in record:
            del record['_id']
        self._buffer.append(record)
        print(f"Buffer size: {len(self._buffer)}")
        if len(self._buffer) >= self._buffer_size:
            self._flush_buffer(collection_name)

    def _flush_buffer(self, collection_name: str) -> None:
        """Flush the buffer to MongoDB"""
        if self._buffer:
            collection = self._db[collection_name]
            try:
                collection.insert_many(self._buffer)
            except BulkWriteError as e:
                print(f"Error inserting records: {e}")
                list(collection.find())
            self._buffer = []

    def aggregate(self, collection_name: str, pipeline: list) -> list:
        """
        Run a MongoDB aggregation pipeline on the specified collection.

        Args:
            collection_name (str): The name of the collection
                to run the aggregation on
            pipeline (list): List of pipeline stages to execute

        Returns:
            list: The results of the aggregation pipeline
        """
        collection = self._db[collection_name]
        return list(collection.aggregate(pipeline))
