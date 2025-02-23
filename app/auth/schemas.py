from pydantic import BaseModel


class UserRegistrationModel(BaseModel):
    username: str
    email: str
    password: str
