from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, SessionLocal

class FundraisingActivity(Base):
    __tablename__ = "fundraising_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    currency = Column(String(10), nullable=False)
    goal_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    category = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    beneficiary_name = Column(String(255), nullable=True)
    fundraiser_name = Column(String(255), nullable=True)
    deadline = Column(String(20), nullable=True)
    status = Column(String(20), default="ACTIVE")
    view_count = Column(Integer, default=0)
    shortlist_count = Column(Integer, default=0)
    fundraiser_id = Column(Integer, ForeignKey("user_accounts.id"), nullable=False)

    