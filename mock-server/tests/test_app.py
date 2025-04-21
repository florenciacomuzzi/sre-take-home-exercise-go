import pytest
from mock_server.app import app
from mock_server.database import Database
from pymongo import MongoClient
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db(monkeypatch):
    # Create a test database
    test_client = MongoClient('mongodb://localhost:27017/')
    test_db = test_client['test_mock_server']
    
    # Mock the Database class
    def mock_get_db():
        return test_db
    
    monkeypatch.setattr(Database, 'db', property(mock_get_db))
    
    yield test_db
    
    # Cleanup
    test_client.drop_database('test_mock_server')
    test_client.close()

def test_get_request(client, mock_db):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['method'] == 'GET'
    
    # Verify the request was logged in MongoDB
    requests = list(mock_db.requests.find())
    assert len(requests) == 1
    assert requests[0]['method'] == 'GET'

def test_post_request(client, mock_db):
    test_data = {'key': 'value'}
    response = client.post('/', json=test_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['method'] == 'POST'
    
    # Verify the request was logged in MongoDB
    requests = list(mock_db.requests.find())
    assert len(requests) == 1
    assert requests[0]['method'] == 'POST'
    assert requests[0]['data'] == test_data 