from sqlalchemy.orm import Session
from app.models.user_account import UserAccount
from app.middleware.auth import verify_password

class LoginCode:
    def __init__(self, db: Session):
        self.db = db

    def validateCredentials(self, email: str, password: str):
        user = self.db.query(UserAccount).filter(UserAccount.email == email).first()

        if not user:
            return {"success": False, "reason": "invalid_credentials"}

        if not verify_password(password, user.password_hash):
            return {"success": False, "reason": "invalid_credentials"}

        if user.status == "SUSPENDED":
            return {"success": False, "reason": "suspended"}

        return {"success": True, "reason": None, "user": user}

    def getUserByEmail(self, email: str):
        return self.db.query(UserAccount).filter(UserAccount.email == email).first()