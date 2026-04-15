from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, SessionLocal
from app.middleware.auth import verify_password, decode_access_token, create_access_token


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    user_profile = relationship("UserProfile", back_populates="accounts")

    @staticmethod
    def _open_db():
        return SessionLocal()

    @staticmethod
    def validateCredentials(email: str, password: str):
        db = UserAccount._open_db()
        try:
            user = db.query(UserAccount).filter(UserAccount.email == email).first()

            if not user:
                return "invalid_credentials"

            if not verify_password(password, user.password_hash):
                return "invalid_credentials"

            if user.status == "SUSPENDED":
                return "suspended"

            token = create_access_token({"sub": str(user.id)})
            role = user.user_profile.name_of_role if user.user_profile else None

            return {
                "token": token,
                "role": role,
            }
        finally:
            db.close()

    @staticmethod
    def invalidateSession(token: str) -> bool:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not user_id:
            return False

        db = UserAccount._open_db()
        try:
            user = db.query(UserAccount).filter(UserAccount.id == int(user_id)).first()
            return user is not None
        finally:
            db.close()