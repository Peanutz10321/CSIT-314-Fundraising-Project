from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from app.models.user_profile import Base
 
load_dotenv()
 
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
 
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
 
def get_db():
    """Dependency — provides a DB session per request, closes after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
def create_tables():
    """Creates all tables defined in models."""
    
    Base.metadata.create_all(bind=engine)