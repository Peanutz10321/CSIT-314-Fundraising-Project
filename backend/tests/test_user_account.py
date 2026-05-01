from conftest import create_test_user, get_or_create_profile, create_auth_headers_for_role
from app.entities.UserAccount import UserAccount

#48 Creating User Account
class TestCreateUserAccount:

    # TC-241-1
    def test_create_user_account_success(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin1@test.com")

        get_or_create_profile(db, "USER_ADMIN")

        response = client.post(
            "/api/user_account/",
            json={
                "name": "Bob",
                "email": "tester123@test.com",
                "password": "tester123",
                "phone_no": "12345678",
                "address": "Clementi Avenue 2",
                "dob": "02-02-2005",
                "user_profile": "USER_ADMIN"
            },
            headers=headers
        )

        assert response.status_code == 201
        body = response.json()
        assert body["email"] == "tester123@test.com"
        assert "password" not in body
        assert "password_hash" not in body
    
    # TC-241-2
    def test_create_duplicate_email_rejected(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin2@test.com")

        get_or_create_profile(db, "FUNDRAISER")
        
        create_test_user(
            db,
            name= "John",
            email= "tester123@test.com",
            password= "tester123",
            role_name= "FUNDRAISER"
        )

        response = client.post(
            "/api/user_account/",
            json={
                "name": "Bob",
                "email": "tester123@test.com",
                "password": "tester123",
                "phone_no": "12345678",
                "address": "Clementi Avenue 2",
                "dob": "02-02-2005",
                "user_profile": "USER_ADMIN"
            },
            headers=headers
        )

        assert response.status_code == 400
    
    # TC-241-3
    def test_create_user_account_missing_fields(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin3@test.com")

        response = client.post(
            "/api/user_account/",
            json={
            "email": "tester123@test.com",
            "password": "tester123",
            "user_profile": "USER_ADMIN"
            },
            headers=headers
        )

        assert response.status_code == 422

#49 Viewing User Account
class TestViewUserAccount:

    # TC-251-1
    def test_view_user_account_success(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin4@test.com")

        user = create_test_user(
            db,
            name= "Bob",
            email= "tester123@test.com",
            password= "tester123",
            role_name= "USER_ADMIN"
        )
        account = db.query(UserAccount).filter(UserAccount.email == "tester123@test.com").first()

        response = client.get(
            f"/api/user_account/{user.id}",
            headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == account.id
        assert body["email"] == "tester123@test.com"
        assert "password_hash" not in body
    
#50 Update User Account
class TestUpdateUserAccount:
    
    # TC-221-1
    def test_update_all_fields_success(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin5@test.com")

        get_or_create_profile(db, "FUNDRAISER")
        create_test_user(
            db,
            name= "Bob",
            email= "tester123@test.com",
            password= "tester123",
            role_name= "USER_ADMIN"
        )
        account = db.query(UserAccount).filter(UserAccount.email == "tester123@test.com").first()


        response = client.patch(
            f"/api/user_account/{account.id}",
            json={
                "name": "Updated name",
                "password": "newpassword123",
                "phone_no": "98765432",
                "address": "Clementi Avenue 3",
                "dob": "01-01-2005",
                "user_profile": "FUNDRAISER"
            },
            headers=headers
        )
 
        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "Updated name"
        assert body["phone_no"] == "98765432"
        assert body["address"] == "Clementi Avenue 3"
        assert body["dob"] == "01-01-2005"
        assert body["status"] == "ACTIVE"
        assert "password" not in body
        assert "password_hash" not in body
    
    #TC-221-2
    def test_partial_update_only_changes_provided_fields(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin6@test.com")

        create_test_user(
            db,
            name="Bob",
            email="tester123@test.com",
            password="tester123",
            phone_no="12345678",
            address="Clementi Avenue 2",
            dob="02-02-2005",
            role_name="USER_ADMIN"
        )
        account = db.query(UserAccount).filter(UserAccount.email == "tester123@test.com").first()

        response = client.patch(
            f"/api/user_account/{account.id}",
            json={
                "name": "Updated name",
                "password": "newpassword123",
                "phone_no": "98765432"
            },
            headers=headers
        )
 
        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "Updated name"
        assert body["phone_no"] == "98765432"
        assert body["address"] == account.address
        assert body["status"] == account.status
        assert body["email"] == account.email

#51 Suspend User Account
class TestSuspendUserAccount:

    # TC-261-1
    def test_suspend_user_account_success(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin7@test.com")

        create_test_user(
            db,
            name="Bob",
            email="tester123@test.com",
            password="tester123",
            phone_no="12345678",
            address="Clementi Avenue 2",
            dob="02-02-2005",
            role_name="USER_ADMIN"
        )
        account = db.query(UserAccount).filter(UserAccount.email == "tester123@test.com").first()

        response = client.patch(
            f"/api/user_account/{account.id}/suspend",
            headers=headers)

        assert response.status_code == 200
        db.expire_all()
        refreshed = db.query(UserAccount).filter(UserAccount.id == account.id).first()
        assert refreshed.status == "SUSPENDED"
        
#52 Search User Accounts
class TestSearchUserAccounts:

    # TC-231-1
    def test_search_user_accounts_by_name(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin8@test.com")

        create_test_user(
            db,
            name="Bob",
            email="tester123@test.com",
            password="tester123",
            phone_no="12345678",
            address="Clementi Avenue 2",
            dob="02-02-2005",
            role_name="USER_ADMIN"
        )

        create_test_user(
            db,
            name="John",
            email="tester124@test.com",
            password="tester124",
            role_name="FUNDRAISER"
        )

        response = client.get(
            "/api/user_account/?keyword=Bob",
            headers=headers)
 
        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 1
        assert all("bob" in a["name"].lower() for a in body["data"])
    
    # TC-231-2
    def test_search_filter_by_name_not_found(self, client, db):
        headers = create_auth_headers_for_role(db, email="admin9@test.com")

        create_test_user(
            db,
            name="Bob",
            email="tester123@test.com",
            password="tester123",
            phone_no="12345678",
            address="Clementi Avenue 2",
            dob="02-02-2005",
            role_name="USER_ADMIN"
        )

        create_test_user(
            db,
            name="John",
            email="tester124@test.com",
            password="tester124",
            role_name="FUNDRAISER"
        )

        response = client.get(
            "/api/user_account/?keyword=random",
            headers=headers)
 
        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []