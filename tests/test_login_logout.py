import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.user_profile import Base, UserProfile, Status, create_user_by_role
from passlib.context import CryptContext


TEST_DATABASE_URL = "sqlite:///./test_auth.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Fresh DB for every test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_test_user(db, email, password, role, status=Status.ACTIVE):
    """Helper to insert a user directly into DB for test setup."""
    hashed = pwd_context.hash(password)
    user = create_user_by_role(
        name="Test User",
        email=email,
        password=hashed,
        role=role,
        description="Test user"
    )
    user.status = status
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Test Case for login
class TestLogin:

    # TC-Login-1
    def test_user_admin_login_success(self, db):
        """User Admin logs in with valid credentials."""
        create_test_user(db, "user123@test.com", "testing123", "USER_ADMIN")

        response = client.post("/api/auth/login", json={
            "email": "user123@test.com",
            "password": "testing123"
        })

        assert response.status_code == 200
        assert "token" in response.json()       
        assert response.json["role"] == "USER_ADMIN"           
        assert "password" not in response.json                 

    # TC-Login-2
    def test_fundraiser_login_success(self, db):
        """Fundraiser logs in and gets correct role token."""
        create_test_user(db, "fundraiser123@test.com", "testing123", "FUNDRAISER")

        response = client.post("/api/auth/login", json={
            "email": "fundraiser123@test.com",
            "password": "testing123"
        })

        assert response.status_code == 200
        assert response.json()["role"] == "FUNDRAISER"
        assert "token" in response.json()

    # TC-Login-3
    def test_donee_login_success(self, db):
        """Donee logs in and gets correct role token."""
        create_test_user(db, "donee123@test.com", "testing123", "DONEE")

        response = client.post("/api/auth/login", json={
            "email": "donee123@test.com",
            "password": "testing123"
        })

        assert response.status_code == 200
        assert response.json()["role"] == "DONEE"
        assert "token" in response.json()

    # TC-Login-4
    def test_platform_manager_login_success(self, db):
        """Platform Manager logs in and gets correct role token."""
        create_test_user(db, "platform123@test.com", "testing123", "PLATFORM_MANAGER")

        response = client.post("/api/auth/login", json={
            "email": "platform123@test.com",
            "password": "testing123"
        })

        assert response.status_code == 200
        assert response.json()["role"] == "PLATFORM_MANAGER"
        assert "token" in response.json()

    # TC-Login-5
    def test_login_wrong_password(self, db):
        """Login rejected when password is wrong."""
        create_test_user(db, "user123@test.com", "correctpassword", "USER_ADMIN")

        response = client.post("/api/auth/login", json={
            "email": "user123@test.com",
            "password": "randomPassword"
        })

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    # TC-Login-6
    def test_login_nonexistent_email(self, db):
        """Login rejected when email does not exist."""
        response = client.post("/api/auth/login", json={
            "email": "testing@test.com",
            "password": "testing123"
        })

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    # TC-Login-7
    def test_login_missing_fields(self, db):
        """Login rejected when required fields are missing."""
        response = client.post("/api/auth/login", json={
            "email": "user123@test.com"
            # no passwordd
        })

        assert response.status_code == 422
    
    # TC-Login-8
    def test_suspended_user_cannot_login(self, db):
        """Suspended user is denied login."""
        
        create_test_user(db, "user123@test.com", "testing123", "FUNDRAISER", Status.SUSPENDED)
        response = client.post("/api/auth/login", json={
            "email": "user123@test.com",
            "password": "testing123"
        })
        assert response.status_code == 403

        assert "suspended" in response.json()["detail"].lower()


# Test Case for logout
class TestLogout:

    def get_token(self, db, email="user@test.com", password="pass123", role="FUNDRAISER"):
        """Helper function to get a token for logout tests."""
        create_test_user(db, email, password, role)
        response = client.post("/api/auth/login", json={
            "email": email,
            "password": password
        })
        return response.json()["token"]

    # TC-Logout-1
    def test_user_admin_logout_success(self, db):
        """A user admin can logout successfully."""
        token = self.get_token(db, "admin@test.com", "admin123", "USER_ADMIN")

        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert "logout" in response.json()["message"].lower()
    
    # TC-Logout-2
    def test_fundraiser_logout_success(self, db):
        """A fundraiser can logout successfully."""
        token = self.get_token(db, "fundraiser123raiser@test.com", "testing123", "FUNDRAISER")
        
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert "logout" in response.json()["message"].lower()
    
    # TC-Logout-3
    def test_donee_logout_success(self, db):
        """A donee can logout successfully."""
        token = self.get_token(db, "donee123@test.com", "testing123", "DONEE")
        
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert "logout" in response.json()["message"].lower()
    
    # TC-Logout-4
    def test_platform_manager_logout_success(self, db):
        """A platform manager can logout successfully."""
        token = self.get_token(db, "platform123@test.com", "testing123", "PLATFORM_MANAGER")
        
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert "logout" in response.json()["message"].lower()