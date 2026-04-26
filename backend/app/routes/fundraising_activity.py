from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.fundraising_activity import (
    FundraisingActivityCreate,
    FundraisingActivityUpdate,
    FundraisingActivityResponse,
    FundraisingActivitySearchResponse,
    ViewCountResponse,
    ShortlistCountResponse,
)
from app.controllers.fundraising_activity import (
    createFundraisingActivityController,
    viewFundraisingActivityController,
    updateFundraisingActivityController,
    getViewCountController,
    getShortlistCountController,
)

router = APIRouter(prefix="/api/fundraising_activity", tags=["Fundraising Activities"])

def require_fundraiser():
    return None

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

@router.get("/{activity_id}/view_count", response_model=ViewCountResponse)
def get_view_count(activity_id: int):
    controller = getViewCountController()
    result = controller.getViewCount(activity_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Activity not found")

    return {"activity_id": activity_id, "view_count": result}


@router.get("/{activity_id}/shortlist_count", response_model=ShortlistCountResponse)
def get_shortlist_count(activity_id: int):
    controller = getShortlistCountController()
    result = controller.getShortlistCount(activity_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Activity not found")

    return {"activity_id": activity_id, "shortlist_count": result}
