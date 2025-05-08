# Create session local, engine and Declarative base with the help of sqlalchemy - connection between MYsql and fastapi
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(url=os.environ.get("DATABASE_URL")) #connect_args = {"check_same_thread":False})

# Create session to connect with db, pass some attributes like autocommit, autoflush and bind
sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Create base

Base = declarative_base()

print("Engine", engine)