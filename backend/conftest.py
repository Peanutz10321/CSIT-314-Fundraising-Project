import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["JWT_SECRET"] = "test-secret"

from app.main import app
from app.database import Base, get_db
from app.entities.UserProfile import UserProfile
from app.entities.UserAccount import UserAccount
from app.middleware.auth import hash_password


TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_user_profile_data():
    return {
        "name_of_role": "FUNDRAISER",
        "description": "People looking to raise funds"
    }


def get_or_create_profile(db, role_name: str):
    profile = db.query(UserProfile).filter(UserProfile.name_of_role == role_name).first()
    if not profile:
        profile = UserProfile(
            name_of_role=role_name,
            description=f"{role_name} profile",
            status="ACTIVE",
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


def create_test_user(db,name: str, email: str,  password: str,  role_name: str, status: str = "ACTIVE", phone_no: str = None, address: str = None, dob: str = None):
    profile = get_or_create_profile(db, role_name)

    user = UserAccount(
        name=name,
        email=email,
        password_hash=hash_password(password),
        user_profile_id=profile.id,
        status=status,
        phone_no=phone_no,
        address=address,
        dob=dob
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user