from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


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