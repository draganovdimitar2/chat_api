from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app.config import Config

pwd_context = CryptContext(schemes=['argon2'])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_data: dict, expiry: timedelta | None = None):
    payload = {
        "user_id": user_data.get('id'),
        "username": user_data.get('username'),
        "exp": datetime.now(timezone.utc) + (expiry if expiry else timedelta(minutes=Config.ACCESS_TOKEN_EXPIRY))
        # 1 hour exp
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.ALGORITHM
    )

    return token

# {
#   "user_id": "some_id",  # example of token output
#   "username": "John",
#   "exp": 1740946347
# }
