from app.__init__ import app
from fastapi.testclient import TestClient

client = TestClient(app)

"""
Test register user endpoint.
NB! TestClient is designed for synchronous code, so to make it work with my asynchronous environment, I need to test each function one by one. 
In the future, I will refactor the tests to use httpx.AsyncClient for true asynchronous testing.
"""


"""
User registration tests
"""


def test_register_user_success():
    response = client.post("auth/register", json={
        "username": "user5",
        "email": "user5@gmail.com",
        "password": "1234"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}


def test_register_user_same_email_error_raises():
    response = client.post("auth/register", json={
        "username": "user6",
        "email": "user@gmail.com",  # we already have a user with this email in db
        "password": "1234"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": 'This email is already in use'}


def test_register_user_same_username_error_raises():
    response = client.post("auth/register", json={
        "username": "user",  # we already have a user with this username
        "email": "user6@gmail.com",
        "password": "1234"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": 'Username already exists'}


def test_register_user_with_invalid_username():
    response = client.post("auth/register", json={
        "username": 123,  # it should raise validation error (username must be str)
        "email": "user6@gmail.com",
        "password": "1234"
    })
    assert response.status_code == 422


def test_register_user_with_invalid_email():
    response = client.post("auth/register", json={
        "username": "user7",
        "email": "user7@",  # it should raise validation error (invalid email)
        "password": "1234"
    })
    assert response.status_code == 422


def test_register_user_with_invalid_password():
    response = client.post("auth/register", json={
        "username": "user7",
        "email": "user7@gmail.com",
        "password": 5896  # it should raise validation error (password must be str)
    })
    assert response.status_code == 422
