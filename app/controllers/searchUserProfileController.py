from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.entities.user_profile_code import UserProfileCode

def searchUserProfile(keyword: str , db: Session):
        code = UserProfileCode(db)
        profiles = code.searchUserProfile(keyword)

        return {
        "total": len(profiles),
        "data": profiles
        }