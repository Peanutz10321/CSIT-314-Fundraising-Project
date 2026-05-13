from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base, get_session


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
    def createUserProfile(name: str, description: str, status: str = "ACTIVE"):
        with get_session() as db:
            existing = db.query(UserProfile).filter(
                UserProfile.name_of_role == name
            ).first()

            if existing:
                return "duplicate_name"

            profile = UserProfile(
                name_of_role=name,
                description=description,
                status=status,
            )

            db.add(profile)
            db.commit()
            db.refresh(profile)

            return profile

    @staticmethod
    def getUserProfileByID(profileID: int):
        with get_session() as db:
            profile = db.query(UserProfile).filter(UserProfile.id == profileID).first()
            if not profile:
                return "not_found"
            return profile

    @staticmethod
    def updateUserProfile(profileID: int, name: str, description: str, status: str = "ACTIVE"):
        with get_session() as db:
            profile = db.query(UserProfile).filter(UserProfile.id == profileID).first()

            if not profile:
                return "not_found"

            duplicate = db.query(UserProfile).filter(
                UserProfile.name_of_role == name,
                UserProfile.id != profileID
            ).first()

            if duplicate:
                return "duplicate_name"

            profile.name_of_role = name
            profile.description = description
            profile.status = status

            db.commit()
            db.refresh(profile)
            return profile

    @staticmethod
    def suspendUserProfile(profileID: int) -> bool:
        with get_session() as db:
            profile = db.query(UserProfile).filter(UserProfile.id == profileID).first()

            if not profile:
                return False

            profile.suspend()
            db.commit()
            return True

    @staticmethod
    def searchUserProfile(keyword: str | None = None):
        with get_session() as db:
            query = db.query(UserProfile)

            if keyword:
                query = query.filter(UserProfile.name_of_role.ilike(f"%{keyword}%"))

            return query.all()
