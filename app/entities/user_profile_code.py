from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile

class UserProfileCode:
    def __init__(self, db: Session):
        self.db = db

    def find_by_name(self, name_of_role: str):
        return self.db.query(UserProfile).filter(
            UserProfile.name_of_role == name_of_role
        ).first()

    def getUserProfileByID(self, profile_id: int):
        return self.db.query(UserProfile).filter(
            UserProfile.id == profile_id
        ).first()

    def createUserProfile(self, name_of_role: str, description: str, status: str = "ACTIVE"):
        profile = UserProfile(
            name_of_role=name_of_role,
            description=description,
            status=status
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return True

    def updateUserProfile(self, profile_id: int, name_of_role: str | None, description: str | None, status: str | None = None):
        profile = self.getUserProfileByID(profile_id)
        if name_of_role is not None:
            profile.name_of_role = name_of_role
        if description is not None:
            profile.description = description
        if status is not None:
            profile.status = status
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def searchUserProfile(self, keyword: str | None = None):
        query = self.db.query(UserProfile)
        if keyword:
            query = query.filter(UserProfile.name_of_role.ilike(f"%{keyword}%"))
        return query.all()
    
    def suspendUserProfile(self, profile_id: int):
        profile = self.getUserProfileByID(profile_id)
        if profile:
            profile.status = "SUSPENDED"
            self.db.commit()
            self.db.refresh(profile)
            return True
        return False