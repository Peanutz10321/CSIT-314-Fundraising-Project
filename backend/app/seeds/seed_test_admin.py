from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile
from app.models.user_account import UserAccount
from app.middleware.auth import hash_password


def seed_test_admin(db: Session) -> None:
    existing = db.query(UserAccount).filter(UserAccount.email == "admin@test.com").first()
    if existing:
        return

    admin_profile = (
        db.query(UserProfile)
        .filter(UserProfile.name_of_role == "USER_ADMIN")
        .first()
    )
    if not admin_profile:
        return

    admin = UserAccount(
        username="admin",
        email="admin@test.com",
        password_hash=hash_password("admin123"),
        user_profile_id=admin_profile.id,
        status="ACTIVE",
    )
    db.add(admin)
    db.commit()