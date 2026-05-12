from sqlalchemy.orm import Session

from app.entities.UserProfile import UserProfile
from app.entities.UserAccount import UserAccount
from app.middleware.auth import hash_password

def seed_test_donee(db: Session) -> None:
    existing = db.query(UserAccount).filter(UserAccount.email == "donee@test.com").first()
    if existing:
        return

    donee_profile = (
        db.query(UserProfile)
        .filter(UserProfile.name_of_role == "DONEE")
        .first()
    )
    if not donee_profile:
        return

    donee = UserAccount(
        name="Donee",
        email="donee@test.com",
        password_hash=hash_password("donee123"),
        user_profile_id=donee_profile.id,
        status="ACTIVE",
    )
    db.add(donee)
    db.commit()
