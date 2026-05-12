from sqlalchemy.orm import Session

from app.entities.UserProfile import UserProfile
from app.entities.UserAccount import UserAccount
from app.middleware.auth import hash_password

def seed_test_fundraiser(db: Session) -> None:
    existing = db.query(UserAccount).filter(UserAccount.email == "fundraiser@test.com").first()
    if existing:
        return

    fundraiser_profile = (
        db.query(UserProfile)
        .filter(UserProfile.name_of_role == "FUNDRAISER")
        .first()
    )
    if not fundraiser_profile:
        return

    fundraiser = UserAccount(
        name="Fundraiser",
        email="fundraiser@test.com",
        password_hash=hash_password("fundraiser123"),
        user_profile_id=fundraiser_profile.id,
        status="ACTIVE",
    )
    db.add(fundraiser)
    db.commit()