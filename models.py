from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import Relationship
from db import Base

# Declarative base is used to define classes mapped to relational database - MySQL here it is
class User(Base):
    __tablename__ = "users" # from declarative_base declared in db script

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(60), unique=True)
    email = Column(String(100),unique=True)
    phone = Column(VARCHAR(10))
    password = Column(String(100000), nullable=False)
    # establish relationship b/w users and blogs table
    blogs = Relationship("Blog", back_populates="creator")


class Blog(Base):
    __tablename__ = "blogs" # from declarative_base

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60))
    body = Column(String(200))
    author = Column(String(30))
    user_id = Column(Integer, ForeignKey('users.id')) # this should be foreign key

    # establish relatiionship between blogs and users table
    creator = Relationship("User", back_populates="blogs") # back_populates - synchronization between both ends 



 
