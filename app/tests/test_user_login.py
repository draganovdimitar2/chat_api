import pytest
from pytest import main


@pytest.mark.asyncio(loop_scope="session")
async def test_user_login_success(async_client):
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "user",
            "password": "1234"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio(loop_scope="session")
async def test_user_login_invalid_username_error_raises(async_client):
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "user1",  # Invalid username
            "password": "1234"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid username/email or password"  # exception detail


@pytest.mark.asyncio(loop_scope="session")
async def test_user_login_invalid_password_error_raises(async_client):
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "user",
            "password": "12345"  # invalid password
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid username/email or password"  # exception detail


@pytest.mark.asyncio(loop_scope="session")
async def test_user_login_invalid_email_error_raises(async_client):
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "user1@gmail.com",  # invalid email
            "password": "12345"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid username/email or password"  # exception detail


if __name__ == "__main__":
    main()
