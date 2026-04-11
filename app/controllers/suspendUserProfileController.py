from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.entities.user_profile_code import UserProfileCode

def suspendUserProfile(profile_id: int, db: Session):
        code = UserProfileCode(db)
        profile = code.getUserProfileByID(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found",
            )

        return code.suspendUserProfile(profile_id)