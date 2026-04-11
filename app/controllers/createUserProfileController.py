from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.entities.user_profile_code import UserProfileCode

def createUserProfile(name_of_role: str, description: str, db: Session, Status: str = "ACTIVE" ):
        code = UserProfileCode(db)
        existing = code.find_by_name(name_of_role)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The name already exists",
            )
        
        return code.createUserProfile(name_of_role, description, Status)