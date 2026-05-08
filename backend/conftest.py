import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.middleware.auth import hash_password, create_access_token

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["JWT_SECRET"] = "test-secret"

from app.main import app
from app.database import Base, get_db
from app.entities.UserProfile import UserProfile
from app.entities.UserAccount import UserAccount
from app.entities.FundraisingCategory import FundraisingCategory


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


def auth_headers(user_id: int):
    token = create_access_token({"sub": str(user_id)})
    return {"Authorization": f"Bearer {token}"}

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

def get_or_create_category(db, name: str = "Education", description: str = None, status: str = "ACTIVE"):
    category = db.query(FundraisingCategory).filter(
        FundraisingCategory.name == name
    ).first()

    if not category:
        category = FundraisingCategory(
            name=name,
            description=description or f"{name} category",
            status=status,
        )
        db.add(category)
        db.commit()
        db.refresh(category)
    else:
        changed = False
        if category.status != status:
            category.status = status
            changed = True
        if description is not None and category.description != description:
            category.description = description
            changed = True
        if changed:
            db.commit()
            db.refresh(category)

    return category

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

def create_test_activity(client, fundraiser_id: int, title: str = "Building a School", **overrides):
    payload = {
        "title": title,
        "description": "Raising funds to help build a primary school",
        "currency": "SGD",
        "goal_amount": 5000.0,
        "category": "Education",
        "location": "Singapore",
        "beneficiaryName": "Bob",
        "fundraiserName": "John",
        "deadline": "29-05-2026",
    }
    payload.update(overrides)

    db = TestingSessionLocal()
    try:
        get_or_create_category(db, payload["category"])
    finally:
        db.close()
    
    return client.post("/api/fundraising_activity/", 
                       json=payload,
                       headers=auth_headers(fundraiser_id),
                       )

def create_completed_activity(
    db,
    fundraiser_id: int,
    title: str = "Building a School",
    category_name: str = "Education",
    **overrides
):
    from app.entities.FundraisingActivity import FundraisingActivity

    category = get_or_create_category(db, category_name)

    activity_data = {
        "fundraiser_id": fundraiser_id,
        "title": title,
        "description": "Raising funds to help build a primary school",
        "currency": "SGD",
        "goal_amount": 5000.0,
        "category_id": category.id,
        "location": "Singapore",
        "beneficiaryName": "Bob",
        "fundraiserName": "John",
        "deadline": "29-05-2026",
        "status": "COMPLETED",
        "current_amount": 0.0,
        "view_count": 0,
        "shortlist_count": 0,
    }
    activity_data.update(overrides)

    activity = FundraisingActivity(**activity_data)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def create_fundraiser(db, name = "John", email = "john@test.com", password = "pass123", role_name = "FUNDRAISER"):
    return create_test_user(
            db,
            name=name,
            email=email,
            password=password,
            role_name=role_name
        )

def create_auth_headers_for_role(
    db,
    name: str = "admin",
    password="admin123",
    role_name: str = "USER_ADMIN",
    email: str = "admin@test.com",
):
    user = create_test_user(
        db=db,
        name=name,
        email=email,
        password=password,
        role_name=role_name,
    )

    return auth_headers(user.id)

def create_donee(db, name = "Jerry", email = "jerry@test.com", password = "testing123", role_name = "DONEE"):
    return create_test_user(
            db,
            name=name,
            email=email,
            password=password,
            role_name=role_name
        )

def create_donee_headers(db):
    donee = create_donee(db)
    return auth_headers(donee.id)

def create_platform_manager(
    db,
    name="Platform Manager",
    email="manager@test.com",
    password="manager123",
    role_name="PLATFORM_MANAGER",
):
    return create_test_user(
        db,
        name=name,
        email=email,
        password=password,
        role_name=role_name,
    )


def create_platform_manager_headers(db):
    manager = create_platform_manager(db)
    return auth_headers(manager.id)


def create_test_category(client, headers, name="Education", description="Schools and learning resources"):
    return client.post(
        "/api/category/",
        json={
            "name": name,
            "description": description,
        },
        headers=headers,
    )

