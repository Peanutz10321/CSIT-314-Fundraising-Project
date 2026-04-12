from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, LogoutResponse
from app.controllers import validateCredentials, invalidateSession

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    result = validateCredentials(db, payload.email, payload.password)

    if not result["success"]:
        if result["reason"] == "suspended":
            raise HTTPException(status_code=403, detail="User account is suspended")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "token": result["token"],
        "role": result["role"],
    }

@router.post("/logout", response_model=LogoutResponse)
def logout(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is required",
        )

    token = authorization.replace("Bearer ", "", 1).strip()

    success = invalidateSession(token, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {
        "message": "Logout successful"
    }
