from unittest.mock import patch

from app.entities.UserProfile import UserProfile

#43 Creating User Profile
class TestCreateUserProfile:

    # TC-95-1
    def test_create_user_success(self, client, sample_user_profile_data):
        with patch("app.routes.user_profile.require_user_admin", return_value=None):
            response = client.post("/api/user_profile/", json=sample_user_profile_data)

        assert response.status_code == 201
        body = response.json()
        assert body["name_of_role"] == "FUNDRAISER"
        assert body["description"] == "People looking to raise funds"
        assert body["status"] == "ACTIVE"
        assert "id" in body
    
    # TC-95-2
    def test_create_user_duplicate_name(self, client, sample_user_profile_data):
        with patch("app.routes.user_profile.require_user_admin", return_value=None):
            client.post("/api/user_profile/", json=sample_user_profile_data)
            response = client.post("/api/user_profile/", json=sample_user_profile_data)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    # TC-95-3
    def test_create_user_missing_required_fields(self, client):
        with patch("app.routes.user_profile.require_user_admin", return_value=None):
            response = client.post("/api/user_profile/", json={"description": "Incomplete"})

        assert response.status_code == 422

#44 Viewing User Profile
class TestViewUserProfile:

    # TC-103-1
    def test_view_user_success(self, client, db, sample_user_profile_data):
        profile = UserProfile(
            name_of_role=sample_user_profile_data["name_of_role"],
            description=sample_user_profile_data["description"],
            status="ACTIVE"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

        with patch("app.routes.user_profile.require_user_admin", return_value=None):
            response = client.get(f"/api/user_profile/{profile.id}")

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == profile.id
        assert body["name_of_role"] == sample_user_profile_data["name_of_role"]
        assert body["description"] == sample_user_profile_data["description"]

#45 Updating User Profile
class TestUpdateUserProfile:

    # TC-110-1
    def test_update_user_success(self, client, db, sample_user_profile_data):
        profile = UserProfile(
            name_of_role=sample_user_profile_data["name_of_role"],
            description=sample_user_profile_data["description"],
            status="ACTIVE"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

        with patch("app.routes.user_profile.require_user_admin", return_value=None):
            response = client.patch(
                f"/api/user_profile/{profile.id}",
                json={"name_of_role": "DONEE", "description": "updated"}
            )

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == profile.id
        assert body["name_of_role"] == "DONEE"
        assert body["description"] == "updated"

#46 Suspend User Profile
class TestSuspendUserProfile:

    #TC-117-1
    def test_suspend_user_success(self, client, db, sample_user_profile_data):
        profile = UserProfile(
            name_of_role=sample_user_profile_data["name_of_role"],
            description=sample_user_profile_data["description"],
            status="ACTIVE"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

        with patch("app.routes.user_profile.require_user_admin", return_value=None):
            response = client.patch(f"/api/user_profile/{profile.id}/suspend")

        assert response.status_code == 200
        assert response.json() == {"success": True}

        db.expire_all()
        refreshed = db.query(UserProfile).filter(UserProfile.id == profile.id).first()
        assert refreshed.status == "SUSPENDED"

#47 Search User Profile
class TestSearchUserProfiles:

    #TC-124-1
    def test_search_filter_by_name(self, client):
        with patch("app.routes.user_profile.require_user_admin", return_value=None):
            client.post("/api/user_profile/", json={
                "name_of_role": "FUNDRAISER",
                "description": "Raise funds"
            })
            client.post("/api/user_profile/", json={
                "name_of_role": "DONEE",
                "description": "Give funds"
            })

            response = client.get("/api/user_profile/?keyword=DONEE")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 1
        assert body["data"][0]["name_of_role"] == "DONEE"

    #TC-124-2
    def test_search_filter_by_name_not_found(self, client):
        with patch("app.routes.user_profile.require_user_admin", return_value=None):
            client.post("/api/user_profile/", json={
                "name_of_role": "FUNDRAISER",
                "description": "Raise funds"
            })
            client.post("/api/user_profile/", json={
                "name_of_role": "DONEE",
                "description": "Give funds"
            })

            response = client.get("/api/user_profile/?keyword=MANAGER")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []
