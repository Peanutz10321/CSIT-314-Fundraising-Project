from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.fundraising_activity import (
    FundraisingActivityCreate,
    FundraisingActivityUpdate,
    FundraisingActivityResponse,
    FundraisingActivitySearchResponse,
)
from app.controllers.fundraising_activity import (
    createFundraisingActivityController,
    viewFundraisingActivityController,
    updateFundraisingActivityController,
    suspendFundraisingActivityController,
    searchFundraisingActivityController,
    searchCompletedActivitiesController,
    viewCompletedActivityController,
)

router = APIRouter(prefix="/api/fundraising_activity", tags=["Fundraising Activities"])

def require_fundraiser():
    return None

@router.get("/", response_model=FundraisingActivitySearchResponse)
def search_fundraising_activities(
    fundraiser_id: int = Query(default=None),
    keyword: str = Query(default=None),
):
    controller = searchFundraisingActivityController()
    activities = controller.searchFundraisingActivities(fundraiser_id, keyword)
    return {
        "total": len(activities),
        "data": activities,
    }


@router.get("/completed", response_model=FundraisingActivitySearchResponse)
def search_completed_activities(fundraiser_id: int = Query(default=None), keyword: str = Query(default=None),):
    controller = searchCompletedActivitiesController()
    activities = controller.searchCompletedActivity(fundraiser_id, keyword)
    return {
        "total": len(activities),
        "data": activities,
    }


@router.get("/completed/{activity_id}", response_model=FundraisingActivityResponse)
def get_completed_activity(activity_id: int):
    controller = viewCompletedActivityController()
    result = controller.getCompletedActivities(activity_id)
    if result == "not_found":
        raise HTTPException(status_code=404, detail="Completed activity not found")
    return result


@router.post("/", response_model=FundraisingActivityResponse, status_code=201)
def create_fundraising_activity(payload: FundraisingActivityCreate):
    controller = createFundraisingActivityController()
    result = controller.createFundraisingActivity(
        payload.fundraiser_id,
        payload.title,
        payload.currency,
        payload.goal_amount,
        payload.category,
        payload.description,
        payload.location,
        payload.beneficiaryName,
        payload.fundraiserName,
        payload.deadline,
    )

    if result == "fundraiser_not_found":
        raise HTTPException(status_code=404, detail="Fundraiser not found")
    if result == "invalid_amount":
        raise HTTPException(status_code=400, detail="goal_amount must be greater than 0")

    return result

@router.get("/{activity_id}", response_model=FundraisingActivityResponse)
def get_fundraising_activity(activity_id: int):
    controller = viewFundraisingActivityController()
    result = controller.viewFundraisingActivity(activity_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Activity not found")

    return result

@router.patch("/{activity_id}/suspend")
def suspend_fundraising_activity(activity_id: int):
    controller = suspendFundraisingActivityController()
    success = controller.suspendFundraisingActivity(activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")

    return {"success": True}


@router.patch("/{activity_id}", response_model=FundraisingActivityResponse)
def update_fundraising_activity(activity_id: int, payload: FundraisingActivityUpdate):
    controller = updateFundraisingActivityController()
    result = controller.updateFundraisingActivity(
        activity_id,
        payload.title,
        payload.currency,
        payload.goal_amount,
        payload.category,
        payload.description,
        payload.location,
        payload.beneficiaryName,
        payload.fundraiserName,
        payload.deadline,
    )

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Activity not found")
    if result == "invalid_amount":
        raise HTTPException(status_code=400, detail="goal_amount must be greater than 0")

    return result
