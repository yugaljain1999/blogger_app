from fastapi import APIRouter, Depends
from fastapi import FastAPI, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional, Annotated
from sqlalchemy.orm import Session
from db import sessionlocal, engine
import models
from pydantic import BaseModel
from fastapi import HTTPException
from schemas import Login
from hashing import Hash
from tokens import create_access_token
from datetime import timedelta

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Bind base models to engine
models.Base.metadata.create_all(bind=engine)
# Create Blog class to not load user details each time we show blogs list to user

# Connect to DB
def get_db():
    db = sessionlocal() # create local db session
    try:
        yield db
    finally:
        db.close()

# specify db dependency - annotated is just to provide extra metadata information about variable, like here ORM session depends on get_db function
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(tags = ['authentication'])


# Login with email or username
@router.post("/login", status_code=status.HTTP_200_OK)
def login(db: db_dependency, request: OAuth2PasswordRequestForm = Depends()): # change request type Login to OauthRequestForm
    # Query db to match login credentials
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail = "Invalid credentials")
    
    # verify plain and encrypted password using passlib bcrypt
    if not Hash.verify(request.password, user.password): # plain_pass and hash_pass
        raise HTTPException(status_code = 404, detail = "Incorrect password")
    
    # Generate JWT token to access other routes
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Adding id attribute too to retrieve access token - 12/5
    access_token = create_access_token(data={"sub":user.email, "id":user.id}, expires_delta = access_token_expires) # generate access token using user email

    return {"access_token":access_token,"token_type":"bearer"}
