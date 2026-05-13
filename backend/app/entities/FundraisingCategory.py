from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base, get_session
from datetime import datetime


class FundraisingCategory(Base):
    __tablename__ = "fundraising_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="ACTIVE", nullable=False)
    date_created = Column(DateTime, default=datetime.now, nullable=False)

    activities = relationship("FundraisingActivity", back_populates="category_ref")

    def suspend(self):
        self.status = "SUSPENDED"

    @staticmethod
    def _activity_count(db, category_id: int) -> int:
        from app.entities.FundraisingActivity import FundraisingActivity

        return db.query(FundraisingActivity).filter(
            FundraisingActivity.category_id == category_id
        ).count()

    @staticmethod
    def _attach_activity_count(db, category):
        category.activity_count = FundraisingCategory._activity_count(db, category.id)
        return category

    @staticmethod
    def createFundraisingCategory(name: str, description: str = None):
        with get_session() as db:
            existing = db.query(FundraisingCategory).filter(
                FundraisingCategory.name == name
            ).first()
            if existing:
                return "duplicate_name"

            category = FundraisingCategory(
                name=name,
                description=description,
                status="ACTIVE",
                date_created=datetime.now(),
            )
            db.add(category)
            db.commit()
            db.refresh(category)

            return FundraisingCategory._attach_activity_count(db, category)

    @staticmethod
    def getCategory(categoryID: int):
        with get_session() as db:
            category = db.query(FundraisingCategory).filter(
                FundraisingCategory.id == categoryID
            ).first()
            if not category:
                return "not_found"

            return FundraisingCategory._attach_activity_count(db, category)

    @staticmethod
    def updateCategory(categoryID: int, name: str = None, description: str = None):
        with get_session() as db:
            category = db.query(FundraisingCategory).filter(
                FundraisingCategory.id == categoryID
            ).first()
            if not category:
                return "not_found"

            if name is not None and name != category.name:
                duplicate = db.query(FundraisingCategory).filter(
                    FundraisingCategory.name == name,
                    FundraisingCategory.id != categoryID,
                ).first()
                if duplicate:
                    return "duplicate_name"
                category.name = name

            if description is not None:
                category.description = description

            db.commit()
            db.refresh(category)

            return FundraisingCategory._attach_activity_count(db, category)

    @staticmethod
    def suspendCategory(categoryID: int) -> bool:
        with get_session() as db:
            category = db.query(FundraisingCategory).filter(
                FundraisingCategory.id == categoryID
            ).first()
            if not category:
                return False
            category.suspend()
            db.commit()
            return True

    @staticmethod
    def searchCategory(query: str = None):
        with get_session() as db:
            dbquery = db.query(FundraisingCategory)
            if query:
                dbquery = dbquery.filter(FundraisingCategory.name.ilike(f"%{query}%"))
            categories = dbquery.order_by(FundraisingCategory.name).all()

            return [
                FundraisingCategory._attach_activity_count(db, category)
                for category in categories
            ]
