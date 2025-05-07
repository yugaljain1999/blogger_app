from fastapi import Depends, FastAPI, HTTPException, status
# import database, models, pydantic, typing
from typing import Annotated
from pydantic import BaseModel
import models
from db import Base, sessionlocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_,or_  # and operation to filter based out of multiple conditions
from fastapi.encoders import jsonable_encoder
from routers import users, blogs, authentication

# Here in main, create pydantic models as class and call through api routing
app = FastAPI(name="blogger")


app.include_router(router=users.router)
app.include_router(router=blogs.router)
app.include_router(router=authentication.router)


# Delete and put(like upsert)

# exclude_unset, exclude_defaults and exclude_none - while calling object, don't return unset, default and none values respectively

# setattr - Set's the value of attribute on an object even though we don't know the attribute value until runtime
"""
class Blog:
    pass
    
blog = Blog() # until here no attribute value on an object, but it sets dynamically value of attribute on object.

setattr(blog, "name", "activist")

print(blog.name)

# Use setattr to partially update fields in db_blog dict without actually knowing fields from update_data

for key,value in update_data.items():
    setattr(db_blog, key, value)

getattr, delattr, hasattr  -->  (obj,name)

class UserBase(BaseModel):
    username: str
    email: str
    phone: int = 87855

user = UserBase(username="dfdf", email="dfd@a.com)

user.model_dump(exclude_unset=True)

print(user)

"""

