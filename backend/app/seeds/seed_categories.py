from sqlalchemy.orm import Session
from app.entities.FundraisingCategory import FundraisingCategory

DEFAULT_CATEGORIES = [
    {"name": "Community", "description": "Community development"},
    {"name": "Education", "description": "Schools and learning resources"},
    {"name": "Disaster", "description": "Disaster relief and recovery"},
    {"name": "Medical", "description": "Healthcare and medical equipment"},
    {"name": "Animals", "description": "Animal welfare"},
]


def seed_categories(db: Session) -> None:
    for data in DEFAULT_CATEGORIES:
        existing = db.query(FundraisingCategory).filter(
            FundraisingCategory.name == data["name"]
        ).first()
        if not existing:
            category = FundraisingCategory(
                name=data["name"],
                description=data["description"],
                status="ACTIVE",
            )
            db.add(category)
    db.commit()
