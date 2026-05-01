from conftest import create_test_user, get_or_create_profile, create_test_activity, create_fundraiser, create_donee
from app.entities.FundraisingActivity import FundraisingActivity

#66 SearchFundraisingActivity
class TestDoneeSearchFundraisingActivity:

    #TC-361-1
    def test_search_activities_by_keyword_success(self, db, client):
        fundraiser = create_fundraiser(db)
        create_test_activity(client, fundraiser.id, title = "Building a School")
        create_test_activity(client, fundraiser.id, title = "Building a Hospital")

        response = client.get("/api/donee/fundraising_activity/?keyword=School")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 1
        assert all("school" in a["title"].lower() for a in body["data"])
        assert all(a["status"] == "ACTIVE" for a in body["data"])
    
    #TC-361-2
    def test_search_no_match_returns_empty(self, db ,client):
        fundraiser = create_fundraiser(db)
        create_test_activity(client, fundraiser.id, title = "Building a School")
        create_test_activity(client, fundraiser.id, title = "Building a Hospital")

        response = client.get("/api/donee/fundraising_activity/?keyword=Random")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []
    
#67 View Fundraising Activity
class TestDoneeViewFundraisingActivity:

    #TC-371-1
    def test_view_fundraising_activity_success(self, db, client):
        fundraiser = create_fundraiser(db)
        created = create_test_activity(client, fundraiser.id, title = "Building a School")
        activity_id = created.json()["id"]

        response = client.get(f"api/donee/fundraising_activity/{activity_id}")

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
    
    #TC-371-2
    def test_view_fundraising_activity_increments_view_count(self, db, client):
        fundraiser = create_fundraiser(db)
        created = create_test_activity(client, fundraiser.id, title = "Building a School")
        activity_id = created.json()["id"]

        response = client.get(f"api/donee/fundraising_activity/{activity_id}")

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == activity_id
        assert body["view_count"] == 1

#68 Save Fundraising Activity
class TestDoneeSaveFundraisingActivity:
    
    #TC-391-1
    def test_donee_save_activity_success(self, db, client):
        fundraiser = create_fundraiser(db)
        donee = create_donee(db)
        created = create_test_activity(client, fundraiser.id, title = "Building a School")
        activity_id = created.json()["id"]

        response = client.post("/api/donee/shortlist/", json={
            "donee_id": donee.id,
            "activity_id": activity_id
        })

        assert response.status_code == 201
        body = response.json()
        assert body["donee_id"] == donee.id
        assert body["activity_id"] == activity_id
    
    #TC-391-2
    def test_donee_save_activity_increments_shortlist_count(self, db, client):
        fundraiser = create_fundraiser(db)
        donee = create_donee(db)
        created = create_test_activity(client, fundraiser.id, title = "Building a School")
        activity_id = created.json()["id"]

        client.post("/api/donee/shortlist/", json={
            "donee_id": donee.id,
            "activity_id": activity_id
        })

        db.expire_all()
        activity = db.query(FundraisingActivity).filter(
            FundraisingActivity.id == activity_id
        ).first()
        assert activity.shortlist_count == 1
    
#69
class TestDoneeSearchFavoritesList:

    #TC-401-1
    def test_search_favorite_activities_by_keyword_success(self, db, client):
        fundraiser = create_fundraiser(db)
        donee = create_donee(db)
        activity1 = create_test_activity(client, fundraiser.id, title = "Building a School")
        activity2 = create_test_activity(client, fundraiser.id, title = "Building a Hospital")
        activity_id1 = activity1.json()["id"]
        activity_id2 = activity2.json()["id"]

        client.post("/api/donee/shortlist/", json={
            "donee_id": donee.id,
            "activity_id": activity_id1
        })
        client.post("/api/donee/shortlist/", json={
            "donee_id": donee.id,
            "activity_id": activity_id2
        })

        response = client.get(f"/api/donee/shortlist/?donee_id={donee.id}&keyword=School")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 1
        assert all("school" in a["title"].lower() for a in body["data"])
    
    #TC-401-2
    def test_search_no_match_returns_empty(self, db, client):
        fundraiser = create_fundraiser(db)
        donee = create_donee(db)
        activity1 = create_test_activity(client, fundraiser.id, title = "Building a School")
        activity2 = create_test_activity(client, fundraiser.id, title = "Building a Hospital")
        activity_id1 = activity1.json()["id"]
        activity_id2 = activity2.json()["id"]

        client.post("/api/donee/shortlist/", json={
            "donee_id": donee.id,
            "activity_id": activity_id1
        })
        client.post("/api/donee/shortlist/", json={
            "donee_id": donee.id,
            "activity_id": activity_id2
        })

        response = client.get(f"/api/donee/shortlist/?donee_id={donee.id}&keyword=Random")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []

#70
class TestDoneeViewFavoritesList:

    #TC-421-1
    def test_donee_view_favorites_list_success(self, db, client):

        fundraiser = create_fundraiser(db)
        donee = create_donee(db)
        activity1 = create_test_activity(client, fundraiser.id, title = "Building a School")
        activity2 = create_test_activity(client, fundraiser.id, title = "Building a Hospital")
        activity_id1 = activity1.json()["id"]
        activity_id2 = activity2.json()["id"]

        client.post("/api/donee/shortlist/", json={
            "donee_id": donee.id,
            "activity_id": activity_id1
        })
        client.post("/api/donee/shortlist/", json={
            "donee_id": donee.id,
            "activity_id": activity_id2
        })

        response = client.get(f"/api/donee/shortlist/?donee_id={donee.id}")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 2
    
    #TC-421-2
    def test_donee_view_empty_favorites(self, db, client):
        fundraiser = create_fundraiser(db)
        donee = create_donee(db)
        create_test_activity(client, fundraiser.id, title = "Building a School")
        create_test_activity(client, fundraiser.id, title = "Building a Hospital")

        response = client.get(f"/api/donee/shortlist/?donee_id={donee.id}")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []
    
#73 Search completed fundraising activities
class TestDoneeSearchCompletedActivities:
    
    #TC-431-1
    def test_search_completed_returns_only_completed_activities_with_matching_keyword(self, db, client):
        fundraiser = create_fundraiser(db)

        completed = FundraisingActivity(
            fundraiser_id=fundraiser.id,
            title="Building a School",
            currency="SGD",
            goal_amount=5000.0,
            status="COMPLETED",
        )

        completed = FundraisingActivity(
            fundraiser_id=fundraiser.id,
            title="Building a Hospital",
            currency="SGD",
            goal_amount=5000.0,
            status="COMPLETED",
        )

        response = client.get("/api/donee/fundraising_activity/completed?keyword=School")
        
        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 1
        assert body["data"] == []
        assert all("school" in a["title"].lower() for a in body["data"])
        assert all(a["status"] == "COMPLETED" for a in body["data"])

    #TC-431-2
    def test_search_completed_returns_no_match_if_no_matching_activities(self, db, client):
        fundraiser = create_fundraiser(db)

        completed = FundraisingActivity(
            fundraiser_id=fundraiser.id,
            title="Building a School",
            currency="SGD",
            goal_amount=5000.0,
            status="COMPLETED",
        )

        create_test_activity(client, fundraiser.id, title = "Building a Hospital")

        response = client.get("/api/donee/fundraising_activity/completed?keyword=Random")
        
        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []

#74 View Completed Activities
class TestDoneeViewCompletedActivities:
    
    def test_view_completed_activities_success(self, db, client):
        fundraiser = create_fundraiser(db)

        completed = FundraisingActivity(
            fundraiser_id=fundraiser.id,
            title="Building a School",
            description="Raising funds to help build a primary school",
            currency="SGD",
            goal_amount=5000.0,
            category="Education",
            location="Singapore",
            beneficiaryName="Bob",
            fundraiserName="John",
            deadline="29-05-2026",
            status="COMPLETED",
        )

        db.add(completed)
        db.commit()
        db.refresh(completed)

        response = client.get(f"/api/donee/fundraising_activity/completed/{completed.id}")
 
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "COMPLETED"
        assert body["title"] == "Building a School"
