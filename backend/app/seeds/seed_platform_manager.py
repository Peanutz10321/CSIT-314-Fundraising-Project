from sqlalchemy.orm import Session
from app.entities.UserProfile import UserProfile
from app.entities.UserAccount import UserAccount
from app.middleware.auth import hash_password


def seed_platform_manager(db: Session) -> None:
    existing = db.query(UserAccount).filter(UserAccount.email == "manager@test.com").first()
    if existing:
        return

    profile = db.query(UserProfile).filter(
        UserProfile.name_of_role == "PLATFORM_MANAGER"
    ).first()
    if not profile:
        return

    manager = UserAccount(
        name="Platform Manager",
        email="manager@test.com",
        password_hash=hash_password("manager123"),
        user_profile_id=profile.id,
        status="ACTIVE",
    )
    db.add(manager)
    db.commit()
