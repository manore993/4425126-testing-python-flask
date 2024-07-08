import utilities
from utilities import user
import pytest

@pytest.fixture
def setup_mock(mocker):
    user.clear()
    user.create_table()
    user.register("jean", "jean@gmail.com", "1234")
    print("lulu")

@pytest.mark.parametrize("name, email, password", [
("toto","toto@gmail.com","toto4242")
])

def test_register_passed(setup_mock, name, email, password):
    result = user.register(name, email, password)
    assert result [1]  == name


@pytest.mark.parametrize("name, email, password", [
("jean","jean@gmail.com","1234")
])

def test_login_passed(setup_mock, name, email, password):
    result = user.login(email,password)
    assert result [1]  == name

def test_login_failed(setup_mock):
    result = user.login("lulu@gmail.com", "lulu7895")
    assert result == None

def test_register_failed(setup_mock):
    result = user.register("jean", "jean@gmail.com", "1234")
    assert result == None

def test_is_email_exists_yes(setup_mock):
    result = user.is_email_exists("jean@gmail.com")
    assert result [1]  == "jean"

def test_is_email_exists_no(setup_mock):
    result = user.is_email_exists("lulu@gmail.com")
    assert result  == None