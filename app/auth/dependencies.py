import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"id": user_id, "username": username}  # You can return a user object or dictionary
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
