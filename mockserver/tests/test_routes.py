import pytest
from flask import Flask
from mockserver.routes import configure_routes
from mockserver.database import Database
import mongomock

@pytest.fixture
def app():
    pid = "test0"
    app = Flask(pid)
    app.config['WINDOW'] = '10'  # 10 seconds window
    app.config['UP_RATIO'] = '0.5'  # 50% uptime
    
    # Use mongomock for testing
    mock_client = mongomock.MongoClient()
    mock_db = mock_client['test_db']
    
    # Monkey patch the Database class to use our mock
    Database._instance = None
    Database._client = mock_client
    Database._db = mock_db
    
    configure_routes(app, Database(), pid)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_root_endpoint_get(client):
    """Test the root endpoint with GET method"""
    response = client.get('/')
    
    # The response should be either 'OK' with 200 or 'FAIL' with 500
    assert response.status_code in [200, 500]
    assert response.data.decode() in ['OK', 'FAIL']

def test_root_endpoint_post(client):
    """Test the root endpoint with POST method"""
    response = client.post('/', json={'test': 'data'})
    
    # The response should be either 'OK' with 200 or 'FAIL' with 500
    assert response.status_code in [200, 500]
    assert response.data.decode() in ['OK', 'FAIL']

def test_root_endpoint_logs_request(client):
    """Test that requests are properly logged to the database"""
    # Make a request
    client.get('/')
    
    # Get the database instance
    db = Database()
    
    # Check that the request was logged
    requests = list(db.db.requests.find({'type': 'request'}))
    assert len(requests) == 1
    
    # Check that the response was logged
    responses = list(db.db.requests.find({'type': 'response'}))
    assert len(responses) == 1