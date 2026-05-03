from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base, SessionLocal
from datetime import datetime


class FavoriteList(Base):
    __tablename__ = "shortlists"

    id = Column(Integer, primary_key=True, index=True)
    donee_id = Column(Integer, ForeignKey("user_accounts.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("fundraising_activities.id"), nullable=False)
    date_saved = Column(DateTime, default=datetime.now, nullable=False)

    donee = relationship("UserAccount", back_populates="shortlists")
    activity = relationship("FundraisingActivity", back_populates="shortlists")

    @staticmethod
    def _open_db():
        return SessionLocal()

    @staticmethod
    def saveFundraisingActivity(doneeID: int, activityID: int):
        from app.entities.FundraisingActivity import FundraisingActivity
        db = FavoriteList._open_db()
        try:

            activity = db.query(FundraisingActivity).filter(
                FundraisingActivity.id == activityID
            ).first()
            if not activity:
                return "activity_not_found"

            existing = db.query(FavoriteList).filter(
                FavoriteList.donee_id == doneeID,
                FavoriteList.activity_id == activityID
            ).first()
            if existing:
                return "already_saved"

            shortlist = FavoriteList(
                donee_id=doneeID,
                activity_id=activityID,
                date_saved=datetime.now()
            )
            db.add(shortlist)

            activity.shortlist_count += 1
            db.commit()
            db.refresh(shortlist)
            return shortlist
        finally:
            db.close()

    @staticmethod
    def searchFavoriteList(doneeID: int, keyword: str = None):
        from app.entities.FundraisingActivity import FundraisingActivity
        db = FavoriteList._open_db()
        try:
            query = db.query(FundraisingActivity).join(
                FavoriteList, FavoriteList.activity_id == FundraisingActivity.id
            ).filter(
                FavoriteList.donee_id == doneeID
            )
            if keyword:
                query = query.filter(
                    FundraisingActivity.title.ilike(f"%{keyword}%")
                )
            return query.all()
        finally:
            db.close()