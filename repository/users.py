from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db import sessionlocal, engine
import models
from schemas import BlogBase, UserBase, ShowBlogBase, ShowUserBase, User
from hashing import Hash
from oauth2 import get_current_user
from datetime import timedelta

from redis_client import redis_client

# Connect to DB
def get_db():
    db = sessionlocal() # create local db session
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


def get_users(db: db_dependency):
    # get all blogs
    users = db.query(models.User).all()
    return users


def create_user(user: User, db: db_dependency):
    hashed_pass = Hash.bcrypt(user.password)
    db_user = models.User(username = user.username, email = user.email, phone = user.phone, password = hashed_pass) # .dict() replaced with model_dump() in pydantic v2
    # Add db user
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int, db: db_dependency):
    # query db by id to get user details
    user = db.query(models.User).filter(models.User.id==user_id).first() # always 1 as it's unique id
    # If no user then return exception 404
    if user is None:
        return HTTPException(status_code=404, detail="User not found")
    return user

def put_user(user: UserBase, db: db_dependency, current_user: models.User = Depends(get_current_user)):
    user_to_update = db.query(models.User).filter(models.User.id == current_user.id).first()
    print(user_to_update.id, user_to_update.email)
    if user_to_update is None:
        return HTTPException(status_code=404, detail="User not found to update")
    # get attributes to update
    update_data = user.model_dump(exclude_unset=True) # don't include default attributes
    for key, value in update_data.items():
        setattr(user_to_update, key, value)    
    # commit and refresh db
    db.commit()
    db.refresh(user_to_update)
    return user_to_update

def delete_user(db: db_dependency, current_user: models.User = Depends(get_current_user)):
    user_to_delete = db.query(models.User).filter(models.User.id == current_user.id).first()
    if user_to_delete is None:
        return HTTPException(status_code = 404, detail = "User not found")
    db.delete(user_to_delete)
    db.commit()
    # Set expiration time of access token to 0 seconds - to immediately not able to access authenticated functions

    # setx value in redis db
    redis_client.setex(f"blacklist:{current_user.id}", timedelta(minutes=30), "revoked")

    return user_to_delete