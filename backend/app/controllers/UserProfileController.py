from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.entities.user_profile_code import UserProfileCode

class UserProfileController:

    def __init__(self, db: Session):
        self.db = db
        self.profileCode = UserProfileCode(db)
        

    def createUserProfile(self,name_of_role: str, description: str, Status: str = "ACTIVE" ):
        existing = self.profileCode.find_by_name(name_of_role)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The name already exists",
            )
        
        return self.profileCode.createUserProfile(name_of_role, description, Status)
    
    def getUserProfileByID(self, profile_id: int):
        profile = self.profileCode.getUserProfileByID(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found",
            )
        return profile
    
    def updateUserProfile(self,profile_id: int, name_of_role : str, description: str, Status : str = "ACTIVE"):
        profile = self.profileCode.getUserProfileByID(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found",
            )

        if name_of_role is not None:
            duplicate = self.profileCode.find_by_name(name_of_role)
            if duplicate and duplicate.id != profile_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The user profile name already exists",
                )
            profile.name_of_role = name_of_role

        if description is not None:
            profile.description = description

        return self.profileCode.updateUserProfile(profile.id, profile.name_of_role, profile.description, profile.status)

    def suspendUserProfile(self,profile_id: int):
        profile = self.profileCode.getUserProfileByID(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found",
            )

        return self.profileCode.suspendUserProfile(profile_id)
    
    def searchUserProfile(self, keyword: str):
        profiles = self.profileCode.searchUserProfile(keyword)

        return {
        "total": len(profiles),
        "data": profiles
        }
    