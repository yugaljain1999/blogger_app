# Create session local, engine and Declarative base with the help of sqlalchemy - connection between MYsql and fastapi
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = "postgresql://neondb_owner:npg_kI5bAlPRp9Qv@ep-quiet-scene-a40sovdq-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
#engine = create_engine(url=os.environ.get("DATABASE_URL")) #connect_args = {"check_same_thread":False})

engine = create_engine(url=database_url, pool_pre_ping=True)

# Create session to connect with db, pass some attributes like autocommit, autoflush and bind
sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Create base

Base = declarative_base()

print("Engine", engine)