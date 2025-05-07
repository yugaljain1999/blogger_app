from fastapi import APIRouter, Depends
from fastapi import FastAPI, status
from typing import List, Optional, Annotated
from sqlalchemy.orm import Session
from db import sessionlocal, engine
import models
from pydantic import BaseModel
from fastapi import HTTPException
from repository import users
from schemas import BlogBase, UserBase, ShowBlogBase, ShowUserBase, User


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

router = APIRouter(tags = ['users'])

# Get users and blogs
@router.get("/users/", status_code=status.HTTP_200_OK, response_model=List[ShowUserBase])
async def get_users(db: db_dependency):
    # get all blogs
    return users.get_users(db)

# Create user
# Make api routing - depends on db_dependency , status_code and response_model - format
@router.post("/users/", status_code=status.HTTP_201_CREATED) # post request to users endpoint and create user
async def create_user(user: User, db: db_dependency):
    return users.create_user(user=user, db=db)

# Get user by user id
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=ShowUserBase)
async def get_user(user_id: int, db: db_dependency):
    # query db by id to get user details
    return users.get_user(user_id=user_id, db=db)

# update user's phone number
@router.put("/users/{id}", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def put_user(id: int, user: UserBase, db: db_dependency):
    return users.put_user(id, user, db)
