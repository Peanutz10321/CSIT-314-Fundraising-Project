import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.user_profile import Base, UserProfile, Role, Status, Fundraiser, Donee, UserAdmin
from unittest.mock import patch


TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    with patch("app.routes.user.require_user_admin", return_value=None):
        yield TestClient(app)


@pytest.fixture
def db():
    """Provide a test DB session."""
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def sample_user_profile_data():
    return {
        "name": "fundraiser",
        "description": "People looking to raise funds"
    }



#43 Creating User Profile
class TestCreateUserProfile:

    # TC-95-1
    def test_create_user_success(self, client, sample_user_profile_data):
        """Admin can create a new user profile."""

        response = client.post("/api/users/", json=sample_user_profile_data)

        assert response.status_code == 201
        assert response.json()["name"] == sample_user_profile_data["name"]
        assert response.json()["description"] == sample_user_profile_data["description"]
        assert response.json()["status"] == "ACTIVE"

    # TC-95-2
    def test_create_user_duplicate_name(self, client, sample_user_profile_data):
        """Cannot create two users with the same name."""

        client.post("/api/users/", json=sample_user_profile_data)

        response = client.post("/api/users/", json=sample_user_profile_data)
        
        assert response.status_code == 400
        assert "The name already exists" in response.json()["detail"]

    # TC-95-3
    def test_create_user_missing_required_fields(self, client):
        """If required fields are missing, user not created"""
        response = client.post("/api/users/", json={"name": "Incomplete"})
        assert response.status_code == 422

#44 Viewing User Profile
class TestViewUserProfile:

    # TC-103-1
    def test_view_user_success(self, client, sample_user_profile_data):
        """Admin can view a user profile."""
        created = client.post("/api/users/", json=sample_user_profile_data).json()

        response = client.get(f"/api/users/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]
        assert response.json()["name"] == sample_user_profile_data["name"]

#45 Updating User Profile
class TestUpdateUserProfile:

    # TC-110-1
    def test_update_user_success(self, client, sample_user_profile_data):
        """Admin can update a user profile information."""
        created = client.post("/api/users/", json=sample_user_profile_data).json()

        response = client.patch(f"/api/users/{created['id']}", json={"name": "Donee", "description": "updated"})
        assert response.status_code == 200
        assert response.json()["name"] == "Donee"
        assert response.json()["description"] == "updated"

#46 Suspend User Profile
class TestSuspendUserProfile:

    #TC-117-1
    def test_suspend_user_success(self, client, sample_user_profile_data):
        """Admin can suspend an active user profile."""
        created = client.post("/api/users/", json=sample_user_profile_data).json()

        response = client.patch(f"/api/users/{created['id']}/suspend")
        assert response.status_code == 200
        assert response.json()["status"] == "SUSPENDED"

#47 Search User Profile
class TestSearchUserProfiles:

    #TC-124-1
    def test_search_filter_by_name(self, client, sample_user_profile_data):
        """Can search user profiles by name."""
        client.post("/api/users/", json=sample_user_profile_data)
        client.post("/api/users/", json={"name": "donee", "description": "I want to give moneyy"})

        response = client.get("/api/users/?name=donee")
        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert response.json()["data"][0]["name"] == "donee"

    #TC-124-2
    def test_search_filter_by_name_not_found(self, client, sample_user_profile_data):
        """Searching returns not found if name doesn't match any user profile"""
        client.post("/api/users/", json=sample_user_profile_data)
        client.post("/api/users/", json={"name": "donee", "description": "I want to give moneyy"})

        response = client.get("/api/users/?name=manager")
        assert response.status_code == 200
        assert response.json()["total"] == 0
        assert response.json()["data"] == []
