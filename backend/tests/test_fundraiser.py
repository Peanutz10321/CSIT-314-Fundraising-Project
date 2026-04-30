from conftest import create_test_user, get_or_create_profile, create_test_activity, create_fundraiser
from app.entities.FundraisingActivity import FundraisingActivity

#55 Creating Fundraising Activity
class TestCreateFundraisingActivity:

    # TC-271-1
    def test_create_activity_success(self, db, client):
        fundraiser = create_fundraiser(db)
 
        response = create_test_activity(client, fundraiser.id)
 
        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "Building a School"
        assert body["description"] == "Raising funds to help build a primary school"    
        assert body["currency"] == "SGD"
        assert body["goal_amount"] == 5000.0
        assert body["category"] == "Education"
        assert body["location"] == "Singapore"
        assert body["beneficiaryName"] == "Bob"
        assert body["fundraiserName"] == "John"
        assert body["deadline"] == "29-05-2026"
        assert body["status"] == "ACTIVE"
    
    # TC-271-2
    def test_create_activity_missing_required_fields(self, client):
        response = client.post("/api/fundraising_activity/", json={
            "title": "Building a School",
            "description": "Raising funds to help build a primary school",
            "currency": "SGD",
            "deadline": "29-05-2026",
        })
 
        assert response.status_code == 422

#56 Viewing Fundraising Activity
class TestViewFundraisingActivity:

    # TC-281-1
    def test_view_activity_success(self, db, client):
        fundraiser = create_fundraiser(db)

        created = create_test_activity(client, fundraiser.id)
        activity_id = created.json()["id"]

        response = client.get(f"/api/fundraising_activity/{activity_id}")

        assert response.status_code == 200
        body = response.json()

        db.expire_all()
        activity = db.query(FundraisingActivity).filter(
            FundraisingActivity.id == activity_id
        ).first()

        assert body["id"] == activity.id
        assert body["title"] == activity.title
        assert body["goal_amount"] == activity.goal_amount
        assert body["currency"] == activity.currency
        assert body["status"] == activity.status

#57 Updating Fundraising Activity
class TestUpdateFundraisingActivity:

    # TC-291-1
    def test_update_all_fields_success(self, db, client):
        fundraiser = create_fundraiser(db)

        created = create_test_activity(client, fundraiser.id)
        activity_id = created.json()["id"]

        response = client.patch(f"/api/fundraising_activity/{activity_id}", json={
            "title": "Building a Hospital",
            "description": "Raising funds to help build a hospital",
            "currency": "SGD",
            "goal_amount": 10000.0,
            "category": "Health",
            "location": "Singapore",
            "beneficiaryName": "Felix",
            "fundraiserName": "Jack",
            "deadline": "20-05-2026",
            })
        
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Building a Hospital"
        assert body["description"] == "Raising funds to help build a hospital"
        assert body["currency"] == "SGD"
        assert body["goal_amount"] == 10000.0
        assert body["category"] == "Health"
        assert body["location"] == "Singapore"
        assert body["beneficiaryName"] == "Felix"
        assert body["fundraiserName"] == "Jack"
        assert body["deadline"] == "20-05-2026"

    # TC-291-2
    def test_partial_update_only_changes_provided_files(self, db, client):
        fundraiser = create_fundraiser(db)

        created = create_test_activity(client, fundraiser.id)
        activity_id = created.json()["id"]

        response = client.patch(f"/api/fundraising_activity/{activity_id}", json={
            "goal_amount": 20000.0,
            "deadline": "20-06-2026",
            })
        
        assert response.status_code == 200
        body = response.json()
        
        assert body["goal_amount"] == 20000.0
        assert body["deadline"] == "20-06-2026"

        assert body["title"] == "Building a School"
        assert body["category"] == "Education"
    
#58 Suspending Fundraising Activity
class TestSuspendFundraisingActivity:

    # TC-301-1
    def test_suspend_activity_success(self, db, client):
        fundraiser = create_fundraiser(db)

        created = create_test_activity(client, fundraiser.id)
        activity_id = created.json()["id"]
 
        response = client.patch(f"/api/fundraising_activity/{activity_id}/suspend")

        assert response.status_code == 200
        db.expire_all()
        refreshed = db.query(FundraisingActivity).filter(FundraisingActivity.id == activity_id).first()
        assert refreshed.status == "SUSPENDED"

#59 Searching Fundraising Activities
class TestSearchFundraisingActivities:

    # TC-311-1
    def test_search_activities_by_title(self, db, client):
        fundraiser = create_fundraiser(db)

        create_test_activity(client, fundraiser.id, title="Building a School")
        create_test_activity(client, fundraiser.id, title="Building a Hospital")

        response = client.get(
            f"/api/fundraising_activity/?fundraiser_id={fundraiser.id}&keyword=Building a School"
        )
 
        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 1
        assert body["data"][0]["title"] == "Building a School"

    #TC-311-2
    def test_search_no_match_returns_empty(self, db, client):
        fundraiser = create_fundraiser(db)

        create_test_activity(client, fundraiser.id, title="Building a School")
        create_test_activity(client, fundraiser.id, title="Building a Hospital")

        response = client.get(
            f"/api/fundraising_activity/?fundraiser_id={fundraiser.id}&keyword=Randomized"
        )

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []

#62 Viewing number of views for Fundraising Activity
class TestActivityViewCount:

    # TC-321-1
    def test_view_increments_view_count(self, db, client):
        fundraiser = create_fundraiser(db)

        created = create_test_activity(client, fundraiser.id)
        activity_id = created.json()["id"]

        first = client.get(f"/api/fundraising_activity/{activity_id}")
        assert first.json()["view_count"] == 1
 
        second = client.get(f"/api/fundraising_activity/{activity_id}")
        assert second.json()["view_count"] == 2

    # TC-321-2
    def test_view_count_starts_at_zero(self, db, client):
        fundraiser = create_fundraiser(db)

        response = create_test_activity(client, fundraiser.id)

        assert response.status_code == 201
        assert response.json()["view_count"] == 0

#63 Viewing number of views for Fundraising Activity
class TestActivityShortlistCount:

    # TC-331-1
    def test_shortlist_count_starts_at_zero(self, db, client):
        fundraiser = create_fundraiser(db)

        response = create_test_activity(client, fundraiser.id)

        assert response.status_code == 201
        assert response.json()["shortlist_count"] == 0

#64 Search completed fundraising activities
class TestSearchCompletedFundraisingActivities:

    # TC-341-1
    def test_search_completed_activities_return_only_completed_activities(self, db, client):
        fundraiser = create_fundraiser(db)

        completed = FundraisingActivity(
            fundraiser_id=fundraiser.id,
            title="Building a School",
            currency="SGD",
            goal_amount=5000.0,
            status="COMPLETED",
            category="Education",
        )
        db.add(completed)
        db.commit()
        active = create_test_activity(client, fundraiser.id, title ="Building a Hospital")

        response = client.get(
            f"/api/fundraising_activity/completed?fundraiser_id={fundraiser.id}"
        )
 
        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 1
        assert all(a["status"] == "COMPLETED" for a in body["data"])
    
    # TC-341-2
    def test_search_completed_activities_no_completed_returns_empty(self, db, client):
        fundraiser = create_fundraiser(db)

        create_test_activity(client, fundraiser.id)
        create_test_activity(client, fundraiser.id, title ="Building a Hospital")

        response = client.get(
            f"/api/fundraising_activity/completed?fundraiser_id={fundraiser.id}"
        )
 
        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []

#65 View completed fundraising activity details
class TestViewCompletedFundraisingActivity:

    # TC-351-1
    def test_view_completed_activity_details_success(self, db, client):
        fundraiser = create_fundraiser(db)
        
        completed = FundraisingActivity(
            fundraiser_id=fundraiser.id,
            title="Building a School",
            description="Raising funds to help build a primary school",
            currency="SGD",
            goal_amount=5000.0,
            status="COMPLETED",
            category="Education",
            location="Singapore",
            beneficiaryName="Bob",
            fundraiserName="John",
            deadline="29-05-2026"
        )
        db.add(completed)
        db.commit()
        db.refresh(completed)
        activity_id = completed.id

        response = client.get(f"/api/fundraising_activity/completed/{activity_id}")
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Building a School"
        assert body["description"] == "Raising funds to help build a primary school"    
        assert body["currency"] == "SGD"
        assert body["goal_amount"] == 5000.0
        assert body["category"] == "Education"
        assert body["location"] == "Singapore"
        assert body["beneficiaryName"] == "Bob"
        assert body["fundraiserName"] == "John"
        assert body["deadline"] == "29-05-2026"
        assert body["status"] == "COMPLETED"