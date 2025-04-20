import pytest
from pytest import main


@pytest.mark.asyncio(loop_scope="session")
async def test_user_login_success(async_client):
    login_response = await async_client.post(
        "/auth/login",
        data={
            "username": "user",
            "password": "1234"
        }
    )
    assert login_response.status_code == 200
    jwt_token = login_response.json().get("access_token")  # getting the token

    change_password_data = {
        "old_password": "1234",
        "new_password": "newpassword123"
    }

    response = await async_client.patch(
        "/auth/changePassword",
        json=change_password_data,
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'Password changed successfully!'}

    login_response = await async_client.post(  # check if the password is changed successfully
        "/auth/login",
        data={
            "username": "user",
            "password": "newpassword123"  # now login with the new password
        }
    )
    assert login_response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_user_login_validation_error_raises(async_client):
    login_response = await async_client.post(
        "/auth/login",
        data={
            "username": "user",
            "password": "1234"
        }
    )
    assert login_response.status_code == 200
    jwt_token = login_response.json().get("access_token")

    change_password_data = {
        "old_password": 1234,  # adding the password as int will raise validation error
        "new_password": "newpassword123"
    }

    response = await async_client.patch(
        "/auth/changePassword",
        json=change_password_data,
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_user_login_success(async_client):
    login_response = await async_client.post(
        "/auth/login",
        data={
            "username": "user",
            "password": "1234"
        }
    )
    assert login_response.status_code == 200
    jwt_token = login_response.json().get("access_token")

    change_password_data = {
        "old_password": "123455665",  # this is not the actual old password
        "new_password": "newpassword123"
    }

    response = await async_client.patch(
        "/auth/changePassword",
        json=change_password_data,
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Old password doesn't match!"


if __name__ == "__main__":
    main()
