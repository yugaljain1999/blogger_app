from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db import sessionlocal, engine
import models
from schemas import BlogBase, UserBase, ShowBlogBase, ShowUserBase

# Connect to DB
def get_db():
    db = sessionlocal() # create local db session
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

# Create blog
def create_blog(blog: BlogBase, db: db_dependency):
    db_blog = models.Blog(**blog.model_dump())
    db.add(db_blog)
    db.commit()
    return db_blog

# Get users and blogs
def get_blogs(db: db_dependency, current_user):
    # get all blogs
    blogs = db.query(models.Blog).filter(models.Blog.user_id==current_user.id).all()
    return blogs

# Get blog by id and user details
def get_blog_id(blog_id: int, db: db_dependency):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if blog is None:
        return HTTPException(status_code=404, detail="blog not found")
    return blog

# Return all blogs of given user_id
def get_blog(id: int, user_id: int, db: db_dependency):
    blogs = db.query(models.Blog).filter(and_(models.Blog.user_id == user_id, models.Blog.id==id)).all()
    if len(blogs)==0:
        return HTTPException(status_code=400, detail="Blog not found for particular user")
    return blogs


def put_blog(id: int, blog:BlogBase, db: db_dependency): # here blog is object
    # Get blog by id which needs to be updated
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog_to_update is None:
        return HTTPException(status_code=400, detail="blog to update not found")
    update_data = blog.model_dump(exclude_unset=True) # get from user input - picks up those attribute to change which will be set by user, won't pick default attributes to update
    for key, value in update_data.items():
        setattr(blog_to_update, key, value) # update to db filtered by user input id
    db.commit()
    db.refresh(blog_to_update) # commit to db
    return blog_to_update


def delete_blog(id:int, db: db_dependency):
    blog_to_delete = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog_to_delete is None:
        return HTTPException(status_code=400, detail="blog not found to delete")
    db.delete(blog_to_delete)
    db.commit()

    return blog_to_delete
