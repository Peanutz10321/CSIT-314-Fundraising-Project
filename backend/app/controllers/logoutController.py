from sqlalchemy.orm import Session
from app.entities.logout_code import LogoutCode

def invalidateSession(token: str, db: Session) -> bool:
    session_code = LogoutCode(db)
    return session_code.invalidateSession(token)