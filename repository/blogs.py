from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db import sessionlocal, engine
import models
from schemas import BlogBase, UserBase, ShowBlogBase, ShowUserBase, PutBlogBase
from oauth2 import get_current_user
from sqlalchemy.sql import and_, or_

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
def create_blog(blog: BlogBase, db: db_dependency, current_user: models.User = Depends(get_current_user)):
    db_blog = models.Blog(author=blog.author, title=blog.title, body=blog.body, user_id=current_user.id)
    db.add(db_blog)
    db.commit()
    return db_blog

# Get users and blogs
def get_blogs(db: db_dependency, current_user: models.User = Depends(get_current_user)):
    # get all blogs
    blogs = db.query(models.Blog).filter(models.Blog.user_id==current_user.id).all()
    return blogs

# Get blog by id and user details
def get_blog_id(blog_id: int, db: db_dependency, current_user: models.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(and_(models.Blog.id==blog_id, models.Blog.user_id==current_user.id)).first()
    if blog is None:
        return HTTPException(status_code=404, detail="blog not found")
    return blog

# Return all blogs of given user_id - all users can access publicly available blogs by given user_id
def get_blog(id: int, user_id: int, db: db_dependency):
    blogs = db.query(models.Blog).filter(and_(models.Blog.user_id == user_id, models.Blog.id==id)).all()
    if len(blogs)==0:
        return HTTPException(status_code=400, detail="Blog not found for particular user")
    return blogs


def put_blog(id: int, blog: PutBlogBase, db: db_dependency, current_user: models.User = Depends(get_current_user)):
    # Try to get the blog by id and current user
    blog_to_update = db.query(models.Blog).filter(
        and_(models.Blog.id == id, models.Blog.user_id == current_user.id)
    ).first()
    update_data = blog.model_dump(exclude_unset=True)
    if blog_to_update is None:
        # Insert new record if not found
        new_blog = models.Blog(
            id=id,
            author=update_data.get("author", ""),
            title=update_data.get("title", ""),
            body=update_data.get("body", ""),
            user_id=current_user.id
        )
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    else:
        # Update existing record
        for key, value in update_data.items():
            setattr(blog_to_update, key, value)
        db.commit()
        db.refresh(blog_to_update)
        return blog_to_update


def delete_blog(id:int, db: db_dependency, current_user: models.User = Depends(get_current_user)):
    blog_to_delete = db.query(models.Blog).filter(and_(models.Blog.id == id, models.Blog.user_id==current_user.id)).first()
    if blog_to_delete is None:
        return HTTPException(status_code=400, detail="blog not found to delete")
    db.delete(blog_to_delete)
    db.commit()

    return blog_to_delete
