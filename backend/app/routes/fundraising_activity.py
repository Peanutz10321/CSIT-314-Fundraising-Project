from fastapi import APIRouter, HTTPException, Query, Depends

from app.middleware.access_control import require_roles

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
    viewSingleCompletedActivityController,
)

router = APIRouter(prefix="/api/fundraising_activity", tags=["Fundraising Activities"])

require_fundraiser = require_roles("FUNDRAISER")

@router.get("/", response_model=FundraisingActivitySearchResponse)
def searchFundraisingActivities(
    keyword: str = Query(default=None),
    current_user = Depends(require_fundraiser)
):
    controller = searchFundraisingActivityController()
    activities = controller.searchFundraisingActivities(current_user.id, keyword)

    return {
        "total": len(activities),
        "data": activities,
    }


@router.get("/completed", response_model=FundraisingActivitySearchResponse)
def searchCompletedActivity(
    keyword: str = Query(default=None),
    current_user = Depends(require_fundraiser)
):
    controller = searchCompletedActivitiesController()
    activities = controller.searchCompletedActivity(current_user.id, keyword)

    return {
        "total": len(activities),
        "data": activities,
    }


@router.get("/completed/all", response_model=FundraisingActivitySearchResponse)
def getCompletedActivities(
    current_user = Depends(require_fundraiser)
):
    controller = viewCompletedActivityController()
    activities = controller.getCompletedActivities(current_user.id)

    return {
        "total": len(activities),
        "data": activities,
    }


@router.post("/", response_model=FundraisingActivityResponse, status_code=201)
def createFundraisingActivity(
    payload: FundraisingActivityCreate,
    current_user = Depends(require_fundraiser)
):
    controller = createFundraisingActivityController()
    result = controller.createFundraisingActivity(
        current_user.id,
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
    
    if result == "category_not_found":
        raise HTTPException(status_code=400, detail="Category not found or inactive")
    
    if result == "invalid_amount":
        raise HTTPException(status_code=400, detail="goal_amount must be greater than 0")

    return result

@router.get("/completed/{activity_id}", response_model=FundraisingActivityResponse)
def viewCompletedActivity(
    activity_id: int,
    current_user = Depends(require_fundraiser)
):
    controller = viewSingleCompletedActivityController()
    result = controller.viewCompletedActivity(current_user.id, activity_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Completed activity not found")

    return result


@router.get("/{activity_id}", response_model=FundraisingActivityResponse)
def viewFundraisingActivity(
    activity_id: int,
    current_user = Depends(require_fundraiser)
):
    controller = viewFundraisingActivityController()
    result = controller.viewFundraisingActivity(current_user.id, activity_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Activity not found")

    return result

@router.patch("/{activity_id}/suspend")
def suspendFundraisingActivity(
    activity_id: int,
    current_user = Depends(require_fundraiser)
):
    controller = suspendFundraisingActivityController()
    success = controller.suspendFundraisingActivity(activity_id, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")

    return {"success": True}


@router.patch("/{activity_id}", response_model=FundraisingActivityResponse)
def updateFundraisingActivity(
    activity_id: int, 
    payload: FundraisingActivityUpdate,
    current_user = Depends(require_fundraiser)
):
    controller = updateFundraisingActivityController()
    result = controller.updateFundraisingActivity(
        current_user.id,
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
    
    if result == "category_not_found":
        raise HTTPException(status_code=400, detail="Category not found or inactive")
    
    if result == "invalid_amount":
        raise HTTPException(status_code=400, detail="goal_amount must be greater than 0")

    return result
