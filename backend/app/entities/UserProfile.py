from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base, SessionLocal


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name_of_role = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="ACTIVE", nullable=False)

    accounts = relationship("UserAccount", back_populates="user_profile")

    def suspend(self):
        self.status = "SUSPENDED"

    def to_dict(self):
        return {
            "id": self.id,
            "name_of_role": self.name_of_role,
            "description": self.description,
            "status": self.status,
        }

    @staticmethod
    def _open_db():
        return SessionLocal()

    @staticmethod
    def createUserProfile(name_of_role: str, description: str, status: str = "ACTIVE"):
        db = UserProfile._open_db()

        try:

            existing = db.query(UserProfile).filter(
                UserProfile.name_of_role == name_of_role
            ).first()

            if existing:
                return "duplicate_name"

            profile = UserProfile(
                name_of_role=name_of_role,
                description=description,
                status=status,
            )

            db.add(profile)
            db.commit()
            db.refresh(profile)

            return profile
        
        finally:
            db.close()

    @staticmethod
    def getUserProfileByID(profile_id: int):
        db = UserProfile._open_db()

        try:

            profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
            if not profile:
                return "not_found"
            return profile
        finally:
            db.close()

    @staticmethod
    def updateUserProfile(profile_id: int, name: str, description: str, status: str = "ACTIVE"):
        db = UserProfile._open_db()

        try:

            profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()

            if not profile:
                return "not_found"

            duplicate = db.query(UserProfile).filter(
                UserProfile.name_of_role == name,
                UserProfile.id != profile_id
            ).first()

            if duplicate:
                return "duplicate_name"

            profile.name_of_role = name
            profile.description = description
            profile.status = status

            db.commit()
            db.refresh(profile)
            return profile
        
        finally:
            db.close()

    @staticmethod
    def suspendUserProfile(profile_id: int) -> bool:
        db = UserProfile._open_db()

        try:

            profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()

            if not profile:
                return False

            profile.suspend()
            db.commit()
            return True
        
        finally:
            db.close()

    @staticmethod
    def searchUserProfile(keyword: str | None = None):
        db = UserProfile._open_db()

        try:
            
            query = db.query(UserProfile)

            if keyword:
                query = query.filter(UserProfile.name_of_role.ilike(f"%{keyword}%"))

            return query.all()
        finally:
            db.close()