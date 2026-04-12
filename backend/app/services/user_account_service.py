from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_account import UserAccount
from app.models.user_profile import UserProfile
from app.middleware.auth import hash_password


def create_user_account(
    db: Session,
    username: str,
    email: str,
    password: str,
    user_profile_id: int,
) -> UserAccount:
    existing_username = (
        db.query(UserAccount)
        .filter(UserAccount.username == username)
        .first()
    )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The username already exists",
        )

    existing_email = (
        db.query(UserAccount)
        .filter(UserAccount.email == email)
        .first()
    )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email already exists",
        )

    profile = (
        db.query(UserProfile)
        .filter(UserProfile.id == user_profile_id)
        .first()
    )
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found",
        )

    if profile.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign a suspended user profile",
        )

    user = UserAccount(
        username=username,
        email=email,
        password_hash=hash_password(password),
        user_profile_id=user_profile_id,
        status="ACTIVE",
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user