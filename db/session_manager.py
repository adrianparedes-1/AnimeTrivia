from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from db.base_orm_model import Base

load_dotenv()
db_uri = os.getenv("DATABASE_URI")
engine = create_engine(db_uri, echo=False)

Base.metadata.create_all(bind=engine)

# making session factory
SessionLocal = sessionmaker(engine)

def get_db():
    db = SessionLocal() #session instance
    try:
        yield db
    finally:
        db.flush()
        db.close()