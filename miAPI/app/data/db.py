from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os 

#1. definir la URL de conexion
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    " postgresql://admin:123456@postgres:5432/DB_miapi"
 )

engine= create_engine(DATABASE_URL)

sessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )
Base= declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()