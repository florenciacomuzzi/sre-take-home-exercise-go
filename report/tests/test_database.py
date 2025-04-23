import pytest
import mongomock

from report import database
from report.database import Database
from report.aggregations import get_uptime_percentage


@pytest.fixture(autouse=True)
def reset_database_instance():
    # Ensure each test gets a fresh singleton
    Database._instance = None
    Database._client = None
    Database._db = None


@pytest.fixture
def mock_mongo_client(monkeypatch):
    """
    Replace the real MongoClient with an in-memory mongomock instance.
    """
    client = mongomock.MongoClient()
    # Patch the import in your Database module
    monkeypatch.setattr(database, 'MongoClient', lambda uri: client)
    return client


def test_aggregate_empty(mock_mongo_client):
    db = Database()
    result = db.aggregate('requests', [])
    assert result == []


def test_aggregate_pipeline(mock_mongo_client):
    pid = 'test0'
    coll = 'requests'
    db = Database()
    # Seed some sample docs
    db.db[coll].insert_many([
        {
            "pid": pid,
            "uuid": "6bobQG38Ml7M",
            "type": "response",
            "timestamp": {
                "$date": "2025-04-22T01:39:59.252Z"
            },
            "status": "success",
            "message": "OK",
            "code": 200
        },
    ])

    pipeline = get_uptime_percentage(pid)
    result = db.aggregate(coll, pipeline)
    assert result == [{'fail': 0,
                       'success': 1,
                       'totalRecords': 1,
                       'uptime': 1.0,
                       'uptimePercentage': 100.0
                       }]
