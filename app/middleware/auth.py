from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_profile import UserProfile, Role
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "test")
ALGORITHM = "HS256"
bearer_scheme = HTTPBearer()


def get_current_user():
    raise HTTPException(status_code=401, detail="Not implemented yet")

def require_user_admin():
    raise HTTPException(status_code=401, detail="Not implemented yet")