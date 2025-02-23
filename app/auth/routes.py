from fastapi import APIRouter, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.params import Depends

from .schemas import UserRegistrationModel
from .service import UserService
from app.db.main import get_session

user_service = UserService()  # an instance object of UserService class
router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register")
async def register_user(user_data: UserRegistrationModel, session: AsyncSession = Depends(get_session)) -> dict:
    """
    Endpoint for user registration.
    """
    user_email = user_data.email
    username = user_data.username

    user_email_exists = await user_service.user_exists(user_email,
                                                       session)  # return a bool based on if user email already exists or not
    username_exists = await user_service.user_exists(username,
                                                     session)  # return a bool based on if username already exists or not
    if username_exists:
        raise HTTPException(status_code=400, detail='Username already exists')
    if user_email_exists:
        raise HTTPException(status_code=400, detail='This email is already in use')
    await user_service.user_registration(user_data, session)
    return {"message": "User registered successfully"}
