from fastapi import APIRouter, Depends
from fastapi import FastAPI, status
from typing import List, Optional, Annotated
from sqlalchemy.orm import Session
from db import sessionlocal, engine
import models
from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy.sql import or_, and_
from repository.blogs import create_blog, get_blogs, get_blog_id, put_blog, get_blog, delete_blog
from schemas import BlogBase, UserBase, ShowBlogBase, ShowUserBase, PutBlogBase
from repository import blogs
from oauth2 import get_current_user

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

router = APIRouter(tags = ['blogs'])


# Create blog
@router.post("/blogs/", status_code=status.HTTP_201_CREATED)
async def create_blog(blog: BlogBase, db: db_dependency, current_user: UserBase = Depends(get_current_user)):
    return blogs.create_blog(blog, db, current_user)

# Get users and blogs
# Test get_current_user authentication here
@router.get("/blogs/", status_code=status.HTTP_200_OK, response_model=List[ShowBlogBase])
async def get_blogs(db: db_dependency, current_user: UserBase = Depends(get_current_user)):     
    # get all blogs
    return blogs.get_blogs(db, current_user)

# Get blog by id and user details
@router.get("/blogs/{id}",status_code=status.HTTP_200_OK, response_model=BlogBase)
async def get_blog_id(blog_id: int, db: db_dependency, current_user: UserBase = Depends(get_current_user)):
    return blogs.get_blog_id(blog_id, db, current_user)

# Return all blogs of given user_id
@router.get("/blogs/{id}/{user_id}", status_code=status.HTTP_200_OK, response_model=List[ShowBlogBase])
async def get_blog(id: int, user_id: int, db: db_dependency, current_user: UserBase = Depends(get_current_user)):
    return blogs.get_blog(id, user_id, db)

@router.put("/blogs/{id}", status_code=status.HTTP_201_CREATED, response_model=BlogBase)
async def put_blog(id: int, blog:PutBlogBase, db: db_dependency, current_user: UserBase = Depends(get_current_user)): # here blog is object
    # Get blog by id which needs to be updated
    return blogs.put_blog(id, blog, db, current_user)


@router.delete("/blogs/{id}", status_code=status.HTTP_200_OK, response_model=BlogBase)  # BlogBase pydantic model
async def delete_blog(id:int, db: db_dependency, current_user: UserBase = Depends(get_current_user)):
    return blogs.delete_blog(id, db, current_user)



