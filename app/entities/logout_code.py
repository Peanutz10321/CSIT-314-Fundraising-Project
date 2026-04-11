from sqlalchemy.orm import Session
from app.models.user_account import UserAccount
from app.middleware.auth import decode_access_token

class LogoutCode:
    def __init__(self, db: Session):
        self.db = db

    def invalidateSession(self, token: str) -> bool:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not user_id:
            return False

        user = self.db.query(UserAccount).filter(UserAccount.id == int(user_id)).first()
        if not user:
            return False

        return True