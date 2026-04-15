from conftest import create_test_user

# Test Case for login
class TestLogin:

    # TC-Login-1
    def test_user_admin_login_success(self, db, client):
        create_test_user(db, "user123@test.com", "testing123", "USER_ADMIN")

        response = client.post("/api/auth/login", json={
            "email": "user123@test.com",
            "password": "testing123"
        })

        assert response.status_code == 200
        body = response.json()
        assert "token" in body
        assert body["role"] == "USER_ADMIN"
        assert "password" not in body

    # TC-Login-2
    def test_fundraiser_login_success(self, db, client):
        create_test_user(db, "fundraiser123@test.com", "testing123", "FUNDRAISER")

        response = client.post("/api/auth/login", json={
            "email": "fundraiser123@test.com",
            "password": "testing123"
        })

        assert response.status_code == 200
        assert response.json()["role"] == "FUNDRAISER"
        assert "token" in response.json()

    # TC-Login-3
    def test_donee_login_success(self, db, client):
        create_test_user(db, "donee123@test.com", "testing123", "DONEE")

        response = client.post("/api/auth/login", json={
            "email": "donee123@test.com",
            "password": "testing123"
        })

        assert response.status_code == 200
        assert response.json()["role"] == "DONEE"
        assert "token" in response.json()

    # TC-Login-4
    def test_platform_manager_login_success(self, db, client):
        create_test_user(db, "platform123@test.com", "testing123", "PLATFORM_MANAGER")

        response = client.post("/api/auth/login", json={
            "email": "platform123@test.com",
            "password": "testing123"
        })

        assert response.status_code == 200
        assert response.json()["role"] == "PLATFORM_MANAGER"
        assert "token" in response.json()

    # TC-Login-5
    def test_login_wrong_password(self, db, client):
        create_test_user(db, "user123@test.com", "correctpassword", "USER_ADMIN")

        response = client.post("/api/auth/login", json={
            "email": "user123@test.com",
            "password": "randomPassword"
        })

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    # TC-Login-6
    def test_login_nonexistent_email(self, db, client):
        response = client.post("/api/auth/login", json={
            "email": "testing@test.com",
            "password": "testing123"
        })

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    # TC-Login-7
    def test_login_missing_fields(self, client):
        response = client.post("/api/auth/login", json={
            "email": "user123@test.com"
        })

        assert response.status_code == 422

    # TC-Login-8
    def test_suspended_user_cannot_login(self, db, client):
        create_test_user(db, "user123@test.com", "testing123", "FUNDRAISER", "SUSPENDED")

        response = client.post("/api/auth/login", json={
            "email": "user123@test.com",
            "password": "testing123"
        })

        assert response.status_code == 403
        assert "suspended" in response.json()["detail"].lower()

# Test Case for logout
class TestLogout:

    def get_token(self, db, client, email="user@test.com", password="pass123", role="FUNDRAISER"):
        create_test_user(db, email, password, role)
        response = client.post("/api/auth/login", json={
            "email": email,
            "password": password
        })
        assert response.status_code == 200
        return response.json()["token"]

    #TC-Logout-1
    def test_user_admin_logout_success(self, db, client):
        token = self.get_token(db, client, "admin@test.com", "admin123", "USER_ADMIN")

        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert "logout" in response.json()["message"].lower()

    #TC-Logout-2
    def test_fundraiser_logout_success(self, db, client):
        token = self.get_token(db, client, "fundraiser123@test.com", "testing123", "FUNDRAISER")

        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert "logout" in response.json()["message"].lower()

    #TC-Logout-3
    def test_donee_logout_success(self, db, client):
        token = self.get_token(db, client, "donee123@test.com", "testing123", "DONEE")

        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert "logout" in response.json()["message"].lower()

    #TC-Logout-4
    def test_platform_manager_logout_success(self, db, client):
        token = self.get_token(db, client, "platform123@test.com", "testing123", "PLATFORM_MANAGER")

        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert "logout" in response.json()["message"].lower()
