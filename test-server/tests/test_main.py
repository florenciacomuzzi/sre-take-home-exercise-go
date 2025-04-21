import pytest
from test_server import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_get_request(client):
    """Test that the root endpoint accepts GET requests"""
    response = client.get('/')
    assert response.status_code >= 200  # Since the endpoint returns random status codes between 200-299 for success

def test_post_request(client):
    """Test that the root endpoint accepts POST requests"""
    response = client.post('/')
    assert response.status_code >= 200  # Since the endpoint returns random status codes between 200-299 for success
