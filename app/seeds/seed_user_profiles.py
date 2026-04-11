from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile


DEFAULT_USER_PROFILES = [
    {
        "name_of_role": "USER_ADMIN",
        "description": "Manages user accounts and user profiles",
    },
    {
        "name_of_role": "FUNDRAISER",
        "description": "Creates and manages fundraising activities",
    },
    {
        "name_of_role": "DONEE",
        "description": "Searches, views, and supports fundraising activities",
    },
    {
        "name_of_role": "PLATFORM_MANAGER",
        "description": "Manages categories and platform reports",
    },
]


def seed_user_profiles(db: Session) -> None:
    for profile_data in DEFAULT_USER_PROFILES:
        existing = (
            db.query(UserProfile)
            .filter(UserProfile.name_of_role == profile_data["name_of_role"])
            .first()
        )
        if not existing:
            profile = UserProfile(
                name_of_role=profile_data["name_of_role"],
                description=profile_data["description"],
                status="ACTIVE",
            )
            db.add(profile)

    db.commit()