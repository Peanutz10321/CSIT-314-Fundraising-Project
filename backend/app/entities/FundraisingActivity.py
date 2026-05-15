from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, joinedload
from app.database import Base, get_session
from datetime import datetime

class FundraisingActivity(Base):
    __tablename__ = "fundraising_activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    currency = Column(String(10), nullable=False)
    goal_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    category_id = Column(Integer, ForeignKey("fundraising_categories.id"), nullable=False)
    location = Column(String(255), nullable=True)
    beneficiaryName = Column(String(255), nullable=True)
    fundraiserName = Column(String(255), nullable=True)
    deadline = Column(String(20), nullable=True)
    status = Column(String(20), default="ACTIVE")
    view_count = Column(Integer, default=0)
    shortlist_count = Column(Integer, default=0)
    fundraiser_id = Column(Integer, ForeignKey("user_accounts.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.now, nullable=False)

    category_ref = relationship("FundraisingCategory", back_populates="activities")
    fundraiser = relationship("UserAccount", back_populates="activities")
    shortlists = relationship("FavoriteList", back_populates="activity")

    @property
    def category(self):
        return self.category_ref.name if self.category_ref else None

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
    def createFundraisingActivity(
        fundraiserID: int,
        title: str,
        currency: str,
        goalAmount: float,
        category: str,
        description: str = None,
        location: str = None,
        beneficiaryName: str = None,
        fundraiserName: str = None,
        deadline: str = None,
    ):
        from app.entities.UserAccount import UserAccount
        from app.entities.FundraisingCategory import FundraisingCategory

        with get_session() as db:
            fundraiser = db.query(UserAccount).filter(
                UserAccount.id == fundraiserID
            ).first()

            category_obj = db.query(FundraisingCategory).filter(
                FundraisingCategory.name == category,
                FundraisingCategory.status == "ACTIVE",
            ).first()

            if not category_obj:
                return "category_not_found"

            if not fundraiser:
                return "fundraiser_not_found"

            if goalAmount <= 0:
                return "invalid_amount"

            activity = FundraisingActivity(
                fundraiser_id=fundraiserID,
                title=title,
                currency=currency,
                goal_amount=goalAmount,
                category_id=category_obj.id,
                description=description,
                location=location,
                beneficiaryName=beneficiaryName,
                fundraiserName=fundraiserName,
                deadline=deadline,
                status="ACTIVE",
                view_count=0,
                shortlist_count=0,
                current_amount=0.0,
                date_created=datetime.now()
            )

            db.add(activity)
            db.commit()
            db.refresh(activity)

            activity = (
                db.query(FundraisingActivity)
                .options(joinedload(FundraisingActivity.category_ref))
                .filter(FundraisingActivity.id == activity.id)
                .first()
            )

            return activity

    @staticmethod
    def viewFundraisingActivity(activityID: int, fundraiserID: int):
        with get_session() as db:
            activity = (db.query(FundraisingActivity)
            .options(joinedload(FundraisingActivity.category_ref))
            .filter(
                FundraisingActivity.id == activityID,
                FundraisingActivity.fundraiser_id == fundraiserID
                ).first()
            )
            if not activity:
                return "not_found"

            return activity

    @staticmethod
    def doneeViewFundraisingActivity(activityID: int):
        with get_session() as db:
            activity = (db.query(FundraisingActivity)
            .options(joinedload(FundraisingActivity.category_ref))
            .filter(
                FundraisingActivity.id == activityID,
                FundraisingActivity.status == "ACTIVE"
                ).first()
            )
            if not activity:
                return "not_found"

            activity.view_count += 1
            db.commit()
            db.refresh(activity)

            return activity

    @staticmethod
    def updateFundraisingActivity(
        fundraiserID: int,
        activityID: int,
        title: str = None,
        currency: str = None,
        goalAmount: float = None,
        category: str = None,
        description: str = None,
        location: str = None,
        beneficiaryName: str = None,
        fundraiserName: str = None,
        deadline: str = None,
    ):
        with get_session() as db:
            activity = db.query(FundraisingActivity).filter(
                FundraisingActivity.id == activityID,
                FundraisingActivity.fundraiser_id == fundraiserID
                ).first()

            if not activity:
                return "not_found"

            if goalAmount is not None and goalAmount <= 0:
                return "invalid_amount"

            if title is not None:
                activity.title = title

            if currency is not None:
                activity.currency = currency

            if goalAmount is not None:
                activity.goal_amount = goalAmount

            if description is not None:
                activity.description = description

            if location is not None:
                activity.location = location

            if beneficiaryName is not None:
                activity.beneficiaryName = beneficiaryName

            if fundraiserName is not None:
                activity.fundraiserName = fundraiserName

            if deadline is not None:
                activity.deadline = deadline

            if category is not None:
                from app.entities.FundraisingCategory import FundraisingCategory

                category_obj = db.query(FundraisingCategory).filter(
                    FundraisingCategory.name == category,
                    FundraisingCategory.status == "ACTIVE",
                ).first()

                if not category_obj:
                    return "category_not_found"

                activity.category_id = category_obj.id

            db.commit()
            db.refresh(activity)

            activity = (
                db.query(FundraisingActivity)
                .options(joinedload(FundraisingActivity.category_ref))
                .filter(FundraisingActivity.id == activity.id)
                .first()
            )

            return activity

    @staticmethod
    def suspendFundraisingActivity(activityID: int, fundraiserID: int):
        with get_session() as db:
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

    @staticmethod
    def searchFundraisingActivity(fundraiserID: int = None, keyword: str = None):
        with get_session() as db:
            query = (db.query(FundraisingActivity)
            .options(joinedload(FundraisingActivity.category_ref))
            .filter(
                FundraisingActivity.status != "COMPLETED"
            )
            )
            if fundraiserID is not None:
                query = query.filter(FundraisingActivity.fundraiser_id == fundraiserID)

            if keyword:
                query = query.filter(FundraisingActivity.title.ilike(f"%{keyword}%"))

            return query.order_by(FundraisingActivity.title).all()

    @staticmethod
    def doneeSearchFundraisingActivity(keyword: str = None):
        with get_session() as db:
            query = (db.query(FundraisingActivity)
            .options(joinedload(FundraisingActivity.category_ref))
            .filter(
                FundraisingActivity.status == "ACTIVE"
            )
            )
            if keyword:
                query = query.filter(FundraisingActivity.title.ilike(f"%{keyword}%"))

            return query.order_by(FundraisingActivity.title).all()

    @staticmethod
    def searchCompletedActivity(fundraiserID: int = None, query: str = None):
        with get_session() as db:
            dbquery = (db.query(FundraisingActivity)
            .options(joinedload(FundraisingActivity.category_ref))
            .filter(FundraisingActivity.status == "COMPLETED")
            )
            if fundraiserID is not None:
                dbquery = dbquery.filter(FundraisingActivity.fundraiser_id == fundraiserID)

            if query:
                dbquery = dbquery.filter(FundraisingActivity.title.ilike(f"%{query}%"))

            return dbquery.order_by(FundraisingActivity.title).all()

    @staticmethod
    def getCompletedActivities(activityID: int, fundraiserID: int = None):
        with get_session() as db:
            query = (db.query(FundraisingActivity)
            .options(joinedload(FundraisingActivity.category_ref))
            .filter(
                FundraisingActivity.id == activityID,
                FundraisingActivity.status == "COMPLETED"
            )
            )
            if fundraiserID is not None:
                query = query.filter(FundraisingActivity.fundraiser_id == fundraiserID)
            activity = query.first()

            if not activity:
                return "not_found"

            return activity

    @staticmethod
    def viewCompletedFundraisingActivities():
        return FundraisingActivity.searchCompletedActivity()
