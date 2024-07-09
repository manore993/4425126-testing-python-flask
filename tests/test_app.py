import pytest
from app import create_app
from utilities import user
from flask import session


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_index_not_connected(client):
    response = client.get('/')
    assert response.status_code == 302
    # TODO 

def test_login_page_access(client):
    response = client.get('/login')
    assert response.status_code == 200
    content = response.data.decode()
    assert "Login User" in content
    assert "Want to create account? Goto" in content
    assert "Register" in content

def test_login_page_email_password_None(client):
    response = client.post('/login', data={} )
    assert response.status_code == 400
    content = response.data.decode()
    assert "Please fill all fields" in content

def test_login_failure(client,mocker):
    mocker.patch("utilities.user.user.login", return_value=None)
    response = client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"} )
    assert response.status_code == 403
    content = response.data.decode()
    assert "Invalid email or password" in content
    
def test_login_success(client,mocker):
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    response = client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"} )
    assert response.status_code == 302
    assert response.location == '/'

def test_login_return_redirect(client,mocker):
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"} )

    response = client.get('/login')
    assert response.status_code == 302
    assert response.location == '/'
    
    