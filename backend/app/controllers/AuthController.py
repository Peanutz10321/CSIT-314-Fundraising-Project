from sqlalchemy.orm import Session
from app.entities.login_code import LoginCode
from app.entities.logout_code import LogoutCode
from app.middleware.auth import create_access_token


class AuthController:
    def __init__(self, db: Session):
        self.db = db
        self.login_code = LoginCode(db)
        self.logout_code = LogoutCode(db)

    def validateCredentials(self, email: str, password: str):
        result = self.login_code.validateCredentials(email, password)

        if not result["success"]:
            return result

        user = result["user"]
        token = create_access_token({"sub": str(user.id)})

        return {
            "success": True,
            "reason": None,
            "token": token,
            "role": user.user_profile.name_of_role if user.user_profile else None,
        }
    
    def invalidateSession(self, token: str) -> bool:
        return self.logout_code.invalidateSession(token)