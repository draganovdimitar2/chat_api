from pydantic import BaseModel, EmailStr


class UserRegistrationModel(BaseModel):
    username: str
    email: EmailStr
    password: str


class ChangeUserPassword(BaseModel):
    old_password: str
    new_password: str

class UserDetailsResponse(BaseModel):
    username: str
    email: str