from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import jwt # For token validation
from jwt.exceptions import PyJWTError
import models
from db import sessionlocal

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key and algorithm used for encoding and decoding JWT tokens
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency to get the database session
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")  # Assuming 'sub' contains the user ID
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        # Fetch the user from the database
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        return user
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")



def test_get_blogs_as_different_user(client, test_db):
    # Authenticate as user A
    user = authenticate_user(client, "bias@abcd.com", "biasness")
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt to fetch blogs belonging to user B
    response = client.get("/blogs/", headers=headers)
    assert response.status_code == 200
    assert all(blog["user_id"] == userA.id for blog in response.json())