from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from app.database import Base, get_session
from app.middleware.auth import verify_password, decode_access_token, create_access_token, hash_password



class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    phone_no = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    dob = Column(String(10), nullable=True)

    user_profile = relationship("UserProfile", back_populates="accounts")
    activities = relationship("FundraisingActivity", back_populates="fundraiser")
    shortlists = relationship("FavoriteList", back_populates="donee")

    @property
    def name_of_role(self):
        return self.user_profile.name_of_role if self.user_profile else None

    def suspend(self):
        self.status = "SUSPENDED"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_no": self.phone_no,
            "address": self.address,
            "dob": self.dob,
            "name_of_role": self.user_profile.name_of_role if self.user_profile else None,
            "status": self.status,
        }

    @staticmethod
    def validateCredentials(email: str, password: str):
        with get_session() as db:
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

    @staticmethod
    def invalidateSession(token: str) -> bool:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not user_id:
            return False

        with get_session() as db:
            user = db.query(UserAccount).filter(UserAccount.id == int(user_id)).first()
            return user is not None

    @staticmethod
    def createUserAccount(name: str, email: str, password: str, userProfile: str, phoneNo: str = None, address: str = None, dob: str = None, status: str = "ACTIVE"):
        from app.entities.UserProfile import UserProfile
        with get_session() as db:
            existing = db.query(UserAccount).filter(UserAccount.email == email).first()

            if existing:
                return "duplicate_email"

            profile = db.query(UserProfile).filter(UserProfile.name_of_role == userProfile).first()

            if not profile:
                return "invalid_profile"

            user = UserAccount(
                name=name,
                email=email,
                password_hash=hash_password(password),
                user_profile_id=profile.id,
                phone_no=phoneNo,
                address=address,
                dob=dob,
                status=status
            )

            db.add(user)
            db.commit()
            db.refresh(user)
            user = (
                db.query(UserAccount)
                .options(joinedload(UserAccount.user_profile))
                .filter(UserAccount.id == user.id)
                .first()
            )
            return user

    @staticmethod
    def viewUserAccount(accountID: int):
        with get_session() as db:
            return (
                db.query(UserAccount)
                .options(joinedload(UserAccount.user_profile))
                .filter(UserAccount.id == accountID)
                .first()
            )

    @staticmethod
    def updateUserAccount(accountID: int, name: str = None, password: str = None, userProfile: str = None, phone_no: str = None, address: str = None, dob: str = None, status: str = None):
        from app.entities.UserProfile import UserProfile
        with get_session() as db:
            user = db.query(UserAccount).filter(UserAccount.id == accountID).first()
            if not user:
                return "not_found"

            if userProfile is not None:
                profile = db.query(UserProfile).filter(UserProfile.name_of_role == userProfile).first()

                if not profile:
                    return "invalid_profile"

                user.user_profile_id = profile.id

            if name is not None:
                user.name = name

            if password is not None:
                user.password_hash = hash_password(password)

            if phone_no is not None:
                user.phone_no = phone_no

            if address is not None:
                user.address = address

            if dob is not None:
                user.dob = dob

            if status is not None:
                user.status = status

            db.commit()
            db.refresh(user)
            user = (
                db.query(UserAccount)
                .options(joinedload(UserAccount.user_profile))
                .filter(UserAccount.id == user.id)
                .first()
            )
            return user

    @staticmethod
    def suspendUserAccount(accountID: int):
        with get_session() as db:
            user = db.query(UserAccount).filter(UserAccount.id == accountID).first()
            if not user:
                return False

            user.suspend()
            db.commit()
            db.refresh(user)
            return True

    @staticmethod
    def searchUserAccount(keyword: str):
        with get_session() as db:
            query = db.query(UserAccount).options(joinedload(UserAccount.user_profile))
            if keyword:
                query = query.filter(
                    (UserAccount.name.ilike(f"%{keyword}%")) |
                    (UserAccount.email.ilike(f"%{keyword}%"))
                )
            return query.order_by(UserAccount.name).all()
