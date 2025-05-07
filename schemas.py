from pydantic import BaseModel
from typing import List, Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None



class Login(BaseModel):
    username: str  # email as username
    password: str


class BlogBase(BaseModel):
    author: str
    title: str
    body: str
    user_id: int

    # create relationship with user to show user details for particular blog
    # creator: UserBase

    class Config():
        orm_mode = True

class User(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None
    password: str

# Pydantic models - typehints and data validation of DB models - Validated user input - input attributes to show
class UserBase(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None

    # Show list of blogs for user
    # blogs: List # here blogs is variable created for relationship b/w blogs and users
    class Config():
        orm_mode = True

# ShowUserBase and ShowBlogBase is to serialize response model format as here orm_mode=True

class ShowUserBase(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None

    # Show list of blogs for user
    blogs: List[BlogBase]=[] # here blogs is variable created for relationship b/w blogs and users
    class Config():
        orm_mode = True

class ShowBlogBase(BaseModel):
    author: str
    title: str
    body: str
    user_id: Optional[int] = None 

    # create relationship with user to show user details for particular blog
    creator: Optional[ShowUserBase] = None

    class Config():
        orm_mode = True
