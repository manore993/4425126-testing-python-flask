import pytest
from app import create_app
from utilities import user, calculation



@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_index_not_connected(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.location == '/login'

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
    
def test_index_userid_not_in_session(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.location == '/login'   

def test_index_render_template_calculation(client,mocker):
    
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"} )
    
    response = client.get('/')
    assert response.status_code == 200
    content = response.data.decode()
    assert "Conversion Page" in content
    assert "Enter Input Value" in content

def test_index_validating_input_noinput(client,mocker):
    
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"} )
    
    response = client.post('/', data={} )
    assert response.status_code == 400
    content = response.data.decode()
    assert "Please enter valid input" in content

@pytest.mark.parametrize("input, base", [
("10", "lk"),
("fze", "14"),
("10", "-10"),
])
def test_index_validating_input_wronginput(client,mocker,input,base):
    
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"} )
    
    response = client.post('/', data={"input":input,"base":base} )
    assert response.status_code == 400
    content = response.data.decode()
    assert "Please enter valid input" in content

def test_index_validating_input(client,mocker):
    
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"} )
    
    response = client.post('/', data={} )
    assert response.status_code == 400
    content = response.data.decode()
    assert "Please enter valid input" in content

def test_index_store_in_database_fail(client,mocker):
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    mocker.patch("utilities.calculation.calculation.add_calculation", return_value=None)
    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"} )


    response = client.post('/', data={"input":"10","base":"10"} )

    assert response.status_code == 200
    content = response.data.decode()
    assert "Could not add in history" in content

def test_index_store_in_database_success(client,mocker):
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"} )
    response = client.post('/', data={"input":"10","base":"10"} )

    assert response.status_code == 200
    content = response.data.decode()
    assert "Result" in content
    assert "Input Value:" in content
    assert "Decimal:" in content
    assert "Binary:" in content
    assert "Hexadecimal:" in content

def test_dashboard_user_not_insession(client):
    response = client.get('/dashboard')
    assert response.status_code == 302
    assert response.location == '/'   

def test_dashboard_user_no_history(client,mocker):

    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    mocker.patch("utilities.calculation.calculation.get_user_history", return_value=None)

    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"})
    response = client.get('/dashboard')
    assert response.status_code == 200
    content = response.data.decode()
    assert "Something went wrong, while loading history" in content

def test_dashboard_user_render_template(client,mocker):

    return_history = [("56", 20)] * 10
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    mocker.patch("utilities.calculation.calculation.get_user_history", return_value=return_history)
    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"})
    response = client.get('/dashboard')
    assert response.status_code == 200
    content = response.data.decode()
    print(content)
    assert "<th>Base</th>" in content

def test_register_user_insession(client,mocker):
    
    mocker.patch("utilities.user.user.login", return_value=[1, "toto"])
    client.post('/login', data={"email":"XX@gmail.com", "password":"xx789456"})
    response = client.get('/register')
    assert response.status_code == 302
    assert response.location == '/'   

def test_register_user_not_insession(client,mocker):
    
    response = client.get('/register')
    content = response.data.decode()
    assert "Register User" in content
    assert "Your Name" in content