from pydantic import BaseModel


class UserRegistrationModel(BaseModel):
    username: str
    email: str
    password: str


class ChangeUserPassword(BaseModel):
    old_password: str
    new_password: str

class UserDetailsResponse(BaseModel):
    username: str
    email: str