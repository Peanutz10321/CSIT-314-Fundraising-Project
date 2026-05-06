from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base, SessionLocal
from datetime import datetime


class FundraisingCategory(Base):
    __tablename__ = "fundraising_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="ACTIVE", nullable=False)
    date_created = Column(DateTime, default=datetime.now, nullable=False)

    def suspend(self):
        self.status = "SUSPENDED"

    @staticmethod
    def _open_db():
        return SessionLocal()

    @staticmethod
    def _activity_count(db, category_name: str) -> int:
        from app.entities.FundraisingActivity import FundraisingActivity
        return db.query(FundraisingActivity).filter(
            FundraisingActivity.category == category_name
        ).count()

    @staticmethod
    def createFundraisingCategory(name: str, description: str = None):
        db = FundraisingCategory._open_db()
        try:
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
            result = {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "status": category.status,
                "date_created": category.date_created,
                "activity_count": 0,
            }
            return result
        finally:
            db.close()

    @staticmethod
    def viewFundraisingCategory(category_id: int):
        db = FundraisingCategory._open_db()
        try:
            category = db.query(FundraisingCategory).filter(
                FundraisingCategory.id == category_id
            ).first()
            if not category:
                return "not_found"
            count = FundraisingCategory._activity_count(db, category.name)
            return {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "status": category.status,
                "date_created": category.date_created,
                "activity_count": count,
            }
        finally:
            db.close()

    @staticmethod
    def updateFundraisingCategory(category_id: int, name: str = None, description: str = None):
        db = FundraisingCategory._open_db()
        try:
            category = db.query(FundraisingCategory).filter(
                FundraisingCategory.id == category_id
            ).first()
            if not category:
                return "not_found"

            if name is not None and name != category.name:
                duplicate = db.query(FundraisingCategory).filter(
                    FundraisingCategory.name == name,
                    FundraisingCategory.id != category_id,
                ).first()
                if duplicate:
                    return "duplicate_name"
                category.name = name

            if description is not None:
                category.description = description

            db.commit()
            db.refresh(category)
            count = FundraisingCategory._activity_count(db, category.name)
            return {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "status": category.status,
                "date_created": category.date_created,
                "activity_count": count,
            }
        finally:
            db.close()

    @staticmethod
    def suspendFundraisingCategory(category_id: int) -> bool:
        db = FundraisingCategory._open_db()
        try:
            category = db.query(FundraisingCategory).filter(
                FundraisingCategory.id == category_id
            ).first()
            if not category:
                return False
            category.suspend()
            db.commit()
            return True
        finally:
            db.close()

    @staticmethod
    def searchFundraisingCategory(keyword: str = None):
        db = FundraisingCategory._open_db()
        try:
            query = db.query(FundraisingCategory)
            if keyword:
                query = query.filter(FundraisingCategory.name.ilike(f"%{keyword}%"))
            categories = query.all()
            result = []
            for c in categories:
                count = FundraisingCategory._activity_count(db, c.name)
                result.append({
                    "id": c.id,
                    "name": c.name,
                    "description": c.description,
                    "status": c.status,
                    "date_created": c.date_created,
                    "activity_count": count,
                })
            return result
        finally:
            db.close()
