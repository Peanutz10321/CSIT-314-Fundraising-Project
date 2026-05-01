from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import joinedload

from app.entities.UserAccount import UserAccount
from app.middleware.auth import decode_access_token


def get_current_user(authorization: str | None = Header(default=None)):

    if not authorization or not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is required",
        )

    token = authorization.replace("Bearer ", "", 1).strip()
    payload = decode_access_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    db = UserAccount._open_db()

    try:

        user = (
            db.query(UserAccount)
            .options(joinedload(UserAccount.user_profile))
            .filter(UserAccount.id == int(user_id))
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account not found",
            )

        if user.status == "SUSPENDED":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is suspended",
            )

        return user

    finally:
        db.close()


def require_roles(*allowed_roles: str):
    
    def role_checker(current_user: UserAccount = Depends(get_current_user)):
        user_role = current_user.name_of_role

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker