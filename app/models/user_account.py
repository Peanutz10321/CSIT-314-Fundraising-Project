from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)

    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    user_profile = relationship("UserProfile", back_populates="accounts")

    def suspend(self):
        self.status = "SUSPENDED"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "status": self.status,
            "user_profile_id": self.user_profile_id,
            "user_profile": self.user_profile.name_of_role if self.user_profile else None,
        }