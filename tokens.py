import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException
from datetime import timedelta, datetime, timezone
import schemas
from redis_client import redis_client

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verify JWT Token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        email = payload.get("sub")
        id = payload.get("id")

        # if user is deleted then check if it's id is stored in revoked database
        if redis_client.exists(f"blacklist:{id}"):
            raise HTTPException(status_code=401, detail="User access revoked")

        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email, id=id)
        return token_data
    except InvalidTokenError:
        raise credentials_exception
        
