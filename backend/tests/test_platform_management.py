from conftest import create_test_user, get_or_create_profile, create_test_activity, create_fundraiser, create_test_category

#75
class TestCreateCategory:

    #TC-411-1
    def test_create_category_success(self, client):
        response = create_test_category(client)

        assert response.status_code == 201
        body = response.json()
        assert body["name"] == "Education"
        assert body["description"] == "Schools and learning resources"
        assert body["status"] == "ACTIVE"

    #TC-411-2
    def test_create_duplicate_name_rejected(self, client):

        create_test_category(client, name = "Education")

        response = create_test_category(client, name = "Education")

        assert response.status_code == 400
        assert "already" in response.json()["detail"].lower()

    #TC-411-3
    def test_create_missing_required_fields_rejected(self, client):

        response = client.post("/api/category/", json={
            "description": "Schools and learning resources"
        })

        assert response.status_code == 422

#76 View categories
class TestViewCategory:

    #TC-451-1
    def view_category_success(self, client):

        created = create_test_category(client)
        category_id = created.json()["id"]

        response = client.get(f"/api/category/{category_id}")

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == category_id
        assert body["name"] == "Education"
        assert body["description"] == "Schools and learning resources"

#77 Update categories
class TestUpdateCategory:

    #TC-462-1
    def test_update_category_success(self, client):

        created = create_test_category(client)
        category_id = created.json()["id"]

        response = client.patch(f"/api/category/{category_id}", json={
            "name": "Medical",
            "description": "Healthcare and medical equipment"
        })

        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "Medical"
        assert body["description"] == "Healthcare and medical equipment"
    
    #TC-462-2
    def test_update_rejects_duplicate_name(self, client):
        
        create_test_category(client)
        created = create_test_category(client, name = "Medical", description = "Healthcare and medical equipment")
        category_id = created.json()["id"]

        response = client.patch(f"/api/category/{category_id}", json={
            "name": "Education",
            "description": "Schools and learning resources"
        })

        assert response.status_code == 400
        assert "already" in response.json()["detail"].lower()

#78 Suspend category
class TestSuspendCategory:
    
    #TC-381-1
    def test_suspend_category_success(self, client):

        created = create_test_category(client)
        category_id = created.json()["id"]

        response = client.patch(f"/api/category/{category_id}/suspend")

        assert response.status_code == 200
        assert response.json()["status"] == "SUSPENDED"
    
#79 Search category
class TestSearchCategories:

    #TC-472-1
    def test_search_categories_by_keyword_success(self, client):

        create_test_category(client, name = "Education", description = "Schools and learning resources")
        create_test_category(client, name = "Hospital", description = "Healthcare and medical equipment")

        response = client.get("/api/category/?keyword=Education")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 1
        assert all("education" in c["name"].lower() for c in body["data"])
    
    #TC-472-2
    def test_search_no_match_returns_empty(self, client):

        create_test_category(client, name = "Education", description = "Schools and learning resources")
        create_test_category(client, name = "Hospital", description = "Healthcare and medical equipment")

        response = client.get("/api/category/?keyword=Random")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []

#82 Generate Daily Report
class TestGenerateDailyReport:

    #TC-482-1
    def test_generate_daily_report_success(self, db, client):
        fundraiser = create_fundraiser(db)
        create_test_activity(client, fundraiser.id)

        response = client.get("/api/report/daily?date=10-05-2026")
 
        assert response.status_code == 200
        body = response.json()
        assert "period" in body
        assert "total_activities" in body
        assert "views" in body
        assert "total_donations" in body

#83 Generate Weekly Report
class TestGenerateWeeklyReport:

    #TC-492-1
    def test_generate_weekly_report_success(self, db, client):
        fundraiser = create_fundraiser(db)
        create_test_activity(client, fundraiser.id)

        response = client.get("/api/report/daily?week_start=10-05-2026")
 
        assert response.status_code == 200
        body = response.json()
        assert "period" in body
        assert "total_activities" in body
        assert "views" in body
        assert "total_donations" in body

#84 Generate Monthly Report
class TestGenerateMonthlyReport:

    #TC-502-1
    def test_generate_monthly_report_success(self, db, client):
        fundraiser = create_fundraiser(db)
        create_test_activity(client, fundraiser.id)

        response = client.get("/api/report/daily?month=05-2026")
 
        assert response.status_code == 200
        body = response.json()
        assert "period" in body
        assert "total_activities" in body
        assert "views" in body
        assert "total_donations" in body

