from fastapi import HTTPException, status
from sqlalchemy.orm import Session  
from app.entities.user_profile_code import UserProfileCode

def updateUserProfile(profile_id: int, name_of_role : str, description: str, db: Session, Status : str = "ACTIVE"):
        code = UserProfileCode(db)
        profile = code.getUserProfileByID(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found",
            )

        if name_of_role is not None:
            duplicate = code.find_by_name(name_of_role)
            if duplicate and duplicate.id != profile_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The user profile name already exists",
                )
            profile.name_of_role = name_of_role

        if description is not None:
            profile.description = description

        return code.updateUserProfile(profile.id, profile.name_of_role, profile.description, profile.status)