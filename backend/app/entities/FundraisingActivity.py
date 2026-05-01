from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base, SessionLocal
from datetime import datetime

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
    beneficiaryName = Column(String(255), nullable=True)
    fundraiserName = Column(String(255), nullable=True)
    deadline = Column(String(20), nullable=True)
    status = Column(String(20), default="ACTIVE")
    view_count = Column(Integer, default=0)
    shortlist_count = Column(Integer, default=0)
    fundraiser_id = Column(Integer, ForeignKey("user_accounts.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.now, nullable=False)

    fundraiser = relationship("UserAccount", back_populates="activities")

    def suspend(self):
        self.status = "SUSPENDED"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "currency": self.currency,
            "goal amount": self.goal_amount,
            "current amount": self.current_amount,
            "category": self.category,
            "location": self.location,
            "beneficiary Name": self.beneficiaryName,
            "fundraiser Name": self.fundraiserName,
            "deadline": self.deadline,
            "view count": self.view_count,
            "shortlist count": self.shortlist_count,
            "status": self.status,
        }
    
    @staticmethod
    def _open_db():
        return SessionLocal()

    @staticmethod
    def createFundraisingActivity(
        fundraiserID: int,
        title: str,
        currency: str,
        goal_amount: float,
        category: str,
        description: str = None,
        location: str = None,
        beneficiaryName: str = None,
        fundraiserName: str = None,
        deadline: str = None,
    ):
        from app.entities.UserAccount import UserAccount
        db = FundraisingActivity._open_db()
        try:

            fundraiser = db.query(UserAccount).filter(
                UserAccount.id == fundraiserID
            ).first()

            if not fundraiser:
                return "fundraiser_not_found"
 
            if goal_amount <= 0:
                return "invalid_amount"

            activity = FundraisingActivity(
                fundraiser_id=fundraiserID,
                title=title,
                currency=currency,
                goal_amount=goal_amount,
                category=category,
                description=description,
                location=location,
                beneficiaryName=beneficiaryName,
                fundraiserName=fundraiserName,
                deadline=deadline,
                status="ACTIVE",
                view_count=0,
                shortlist_count=0,
                current_amount=0.0,
                date_created= datetime.now()
            )

            db.add(activity)
            db.commit()
            db.refresh(activity)
            return activity
        finally:
            db.close()
    
    @staticmethod
    def viewFundraisingActivity(activityID: int, fundraiserID: int):

        db = FundraisingActivity._open_db()
        try:

            activity = db.query(FundraisingActivity).filter(
                FundraisingActivity.id == activityID,
                FundraisingActivity.fundraiser_id == fundraiserID
                ).first()
            
            if not activity:
                return "not_found"
            
            return activity
        finally:
            db.close()
    
    @staticmethod
    def updateFundraisingActivity(
        activityID: int,
        fundraiserID: int,
        title: str = None,
        currency: str = None,
        goal_amount: float = None,
        category: str = None,
        description: str = None,
        location: str = None,
        beneficiaryName: str = None,
        fundraiserName: str = None,
        deadline: str = None,
    ):
        db = FundraisingActivity._open_db()
        try:

            activity = db.query(FundraisingActivity).filter(
                FundraisingActivity.id == activityID,
                FundraisingActivity.fundraiser_id == fundraiserID
                ).first()
            
            if not activity:
                return "not_found"

            if goal_amount is not None and goal_amount <= 0:
                return "invalid_amount"
            
            if title is not None:
                activity.title = title

            if currency is not None:
                activity.currency = currency

            if goal_amount is not None:
                activity.goal_amount = goal_amount

            if description is not None:
                activity.description = description

            if category is not None:
                activity.category = category

            if location is not None:
                activity.location = location

            if beneficiaryName is not None:
                activity.beneficiaryName = beneficiaryName

            if fundraiserName is not None:
                activity.fundraiserName = fundraiserName

            if deadline is not None:
                activity.deadline = deadline
 
            db.commit()
            db.refresh(activity)
            return activity
        
        finally:
            db.close()

    @staticmethod
    def suspendFundraisingActivity(activityID: int, fundraiserID: int):
        db = FundraisingActivity._open_db()

        try:

            activity = db.query(FundraisingActivity).filter(
                FundraisingActivity.id == activityID,
                FundraisingActivity.fundraiser_id == fundraiserID
                ).first()
            
            if not activity:
                return False
            
            activity.suspend()
            db.commit()
            db.refresh(activity)
            return True
        finally:
            db.close()

    @staticmethod
    def searchFundraisingActivities(fundraiserID: int = None, keyword: str = None):
        db = FundraisingActivity._open_db()

        try:

            query = db.query(FundraisingActivity).filter(
                FundraisingActivity.status != "COMPLETED"
            )

            if fundraiserID is not None:
                query = query.filter(FundraisingActivity.fundraiser_id == fundraiserID)

            if keyword:
                query = query.filter(FundraisingActivity.title.ilike(f"%{keyword}%"))
            results = query.all()

            return results
        finally:
            db.close()

    @staticmethod
    def searchCompletedActivity(fundraiserID: int = None, query: str = None):
        db = FundraisingActivity._open_db()
        try:
            dbquery = db.query(FundraisingActivity).filter(FundraisingActivity.status == "COMPLETED")

            if fundraiserID is not None:
                dbquery = dbquery.filter(FundraisingActivity.fundraiser_id == fundraiserID)

            if query:
                dbquery = dbquery.filter(FundraisingActivity.title.ilike(f"%{query}%"))

            results = dbquery.all()

            return results
        finally:
            db.close()

    @staticmethod
    def getCompletedActivities(activityID: int, fundraiserID: int):
        db = FundraisingActivity._open_db()

        try:
            
            activity = db.query(FundraisingActivity).filter(
                FundraisingActivity.id == activityID,
                FundraisingActivity.fundraiser_id == fundraiserID,
                FundraisingActivity.status == "COMPLETED"
            ).first()

            if not activity:
                return "not_found"
            
            return activity
        finally:
            db.close()
