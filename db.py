# Create session local, engine and Declarative base with the help of sqlalchemy - connection between MYsql and fastapi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL =  "postgresql://neondb_owner:npg_kI5bAlPRp9Qv@ep-quiet-scene-a40sovdq-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"            # 'sqlite:///output.db'  # "mysql+pymysql://root:root9896@127.0.0.1:3306/BlogApp"  

engine = create_engine(url=DATABASE_URL) #connect_args = {"check_same_thread":False})

# Create session to connect with db, pass some attributes like autocommit, autoflush and bind
sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Create base

Base = declarative_base()

print("Engine", engine)