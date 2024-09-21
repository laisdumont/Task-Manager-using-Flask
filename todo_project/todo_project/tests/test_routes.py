import pytest
from todo_project import app as flaskApp

@pytest.fixture()
def app():
    app = flaskApp
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def test_client(app):
    return app.test_client()

def test_about_route(test_client):
    response = test_client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

def test_register_route(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200

def test_login_route(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200

def test_index_route(test_client):
    response = test_client.get('/')
    assert response.status_code == 200