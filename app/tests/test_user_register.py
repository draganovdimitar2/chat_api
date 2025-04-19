import pytest
from pytest import main


@pytest.mark.asyncio(loop_scope="session")
async def test_user_register_success(async_client):
    response = await async_client.post(
        "/auth/register",
        json={
            "username": "user1",
            "email": "user1@gmail.com",
            "password": "1234"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}


@pytest.mark.asyncio(loop_scope="session")
async def test_user_register_with_same_username_error_raises(async_client):
    response = await async_client.post(
        "/auth/register",
        json={
            "username": "user1",  # same username
            "email": "user5@gmail.com",
            "password": "12346"
        }
    )
    assert response.status_code == 400
    assert response.json()['detail'] == 'Username already exists'


@pytest.mark.asyncio(loop_scope="session")
async def test_user_register_with_same_email_error_raises(async_client):
    response = await async_client.post(
        "/auth/register",
        json={
            "username": "user2",
            "email": "user1@gmail.com",  # the same emails as user1
            "password": "123467"
        }
    )
    assert response.status_code == 400
    assert response.json()['detail'] == "This email is already in use"


@pytest.mark.asyncio(loop_scope="session")
async def test_user_register_with_fake_email_validation_error_raises(async_client):
    response = await async_client.post(
        "/auth/register",
        json={
            "username": "user3",
            "email": "user1",  # not providing correct email
            "password": "1234678"
        }
    )
    assert response.status_code == 422  # code for validation error


if __name__ == "__main__":
    main()
