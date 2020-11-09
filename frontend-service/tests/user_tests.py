import pytest
from app import app

@pytest.fixture
def app_start():
    app = run.create_app({
        'TESTING': True
    })

    yield app


@pytest.fixture
def client(app_start):
    return app_start.test_client()

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

def test_get_auction_list(client):
    response = client.get('/')
    assert response.status_code == 200
