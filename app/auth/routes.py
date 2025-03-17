from fastapi import APIRouter, HTTPException
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .schemas import UserRegistrationModel
from .service import UserService
from .dependencies import get_current_user
from app.db.main import get_session
from app.auth.utils import create_access_token

user_service = UserService()  # an instance object of UserService class
router = APIRouter(prefix='/auth', tags=['Auth'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

session_dependency = Annotated[AsyncSession, Depends(get_session)]
current_user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/register")
async def register_user(user_data: UserRegistrationModel, session: session_dependency) -> dict:
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


@router.post("/login")
async def login(session: session_dependency,
                form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)) -> dict:
    """
    Endpoint for user login. Returns a JWT token if credentials are valid.
    """
    user = await user_service.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username/email or password")

    access_token = create_access_token({"id": user.id, "username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_current_user(current_user: current_user_dependency):
    return current_user
