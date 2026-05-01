from conftest import create_auth_headers_for_role
from app.entities.UserProfile import UserProfile

#43 Creating User Profile
class TestCreateUserProfile:

    # TC-95-1
    def test_create_user_success(self, client, sample_user_profile_data, db):
       
        headers = create_auth_headers_for_role(db, email="admin1@test.com")
        
        response = client.post("/api/user_profile/", 
                               json=sample_user_profile_data,
                               headers=headers)

        assert response.status_code == 201
        body = response.json()
        assert body["name_of_role"] == "FUNDRAISER"
        assert body["description"] == "People looking to raise funds"
        assert body["status"] == "ACTIVE"
        assert "id" in body
    
    # TC-95-2
    def test_create_user_duplicate_name(self, client, sample_user_profile_data, db):
        headers = create_auth_headers_for_role(db, email="admin2@test.com")
    

        client.post("/api/user_profile/", 
                    json=sample_user_profile_data,
                    headers=headers)

        response = client.post("/api/user_profile/", 
                               json=sample_user_profile_data,
                               headers=headers)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    # TC-95-3
    def test_create_user_missing_required_fields(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin3@test.com")

        response = client.post("/api/user_profile/", 
                               json={"Description": "Incomplete"},
                               headers=headers)
            

        assert response.status_code == 422

#44 Viewing User Profile
class TestViewUserProfile:

    # TC-103-1
    def test_view_user_success(self, client, db, sample_user_profile_data):
        headers = create_auth_headers_for_role(db, email="admin4@test.com")

        create_response = client.post(
            "/api/user_profile/",
            json=sample_user_profile_data,
            headers=headers,
        )
        
        profile_id = create_response.json()["id"]

        

        response = client.get(
            f"/api/user_profile/{profile_id}",
            headers=headers
            )

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == profile_id
        assert body["name_of_role"] == sample_user_profile_data["name_of_role"]
        assert body["description"] == sample_user_profile_data["description"]

#45 Updating User Profile
class TestUpdateUserProfile:

    # TC-110-1
    def test_update_user_success(self, client, db, sample_user_profile_data):
        headers = create_auth_headers_for_role(db, email="admin5@test.com")

        create_response = client.post(
            "/api/user_profile/",
            json=sample_user_profile_data,
            headers=headers,
        )

        profile_id = create_response.json()["id"]

        response = client.patch(
            f"/api/user_profile/{profile_id}",
            json={
                "name_of_role": "new name", 
                "description": "new bio"
            },
            headers=headers,
        )

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == profile_id
        assert body["name_of_role"] == "new name"
        assert body["description"] == "new bio"

#46 Suspend User Profile
class TestSuspendUserProfile:

    #TC-117-1
    def test_suspend_user_success(self, client, db, sample_user_profile_data):
        headers = create_auth_headers_for_role(db, email="admin6@test.com")

        create_response = client.post(
            "/api/user_profile/",
            json=sample_user_profile_data,
            headers=headers,
        )

        profile_id = create_response.json()["id"]

        response = client.patch(
            f"/api/user_profile/{profile_id}/suspend",
            headers=headers,
        )

        assert response.status_code == 200
        assert response.json() == {"success": True}

        db.expire_all()
        refreshed = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
        assert refreshed.status == "SUSPENDED"

#47 Search User Profile
class TestSearchUserProfiles:

    #TC-124-1
    def test_search_filter_by_name(self, client, db, sample_user_profile_data):

        headers = create_auth_headers_for_role(db, email="admin7@test.com")

        client.post(
            "/api/user_profile/",
            json=sample_user_profile_data,
            headers=headers,
        )

        client.post(
            "/api/user_profile/",
            json={
            "name_of_role": "DONEE",
            "description": "Give funds"
            },
            headers=headers
        )

        response = client.get(
            "/api/user_profile/?keyword=Fundraiser", 
            headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 1
        assert body["data"][0]["name_of_role"] == "FUNDRAISER"

    #TC-124-2
    def test_search_filter_by_name_not_found(self, client, db, sample_user_profile_data):
        headers = create_auth_headers_for_role(db, email="admin7@test.com")

        client.post(
            "/api/user_profile/",
            json=sample_user_profile_data,
            headers=headers,
        )

        client.post("/api/user_profile/", json={
            "name_of_role": "DONEE",
            "description": "Give funds"
        })

        response = client.get(
            "/api/user_profile/?keyword=Student", 
            headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []
