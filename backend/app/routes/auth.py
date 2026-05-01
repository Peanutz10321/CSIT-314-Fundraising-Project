from fastapi import APIRouter, Header, HTTPException, status
from app.schemas.auth import LoginRequest, LoginResponse, LogoutResponse
from app.controllers.user_account import loginController, logoutController

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):

    controller = loginController()
    result = controller.validateCredentials(payload.email, payload.password)

    if result == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is suspended",
        )

    if result == "invalid_credentials":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return result


@router.post("/logout", response_model=LogoutResponse)
def logout(authorization: str | None = Header(default=None)):
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is required",
        )

    token = authorization.replace("Bearer ", "", 1).strip()

    controller = logoutController()
    success = controller.invalidateSession(token)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {"message": "Logout successful"}