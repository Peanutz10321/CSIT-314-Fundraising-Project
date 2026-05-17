from fastapi import APIRouter, HTTPException, Query, Depends
from app.schemas.donee import (
    ShortlistCreate,
    ShortlistResponse,
    FavoritesSearchResponse,
)
from app.schemas.fundraising_activity import (
    FundraisingActivityResponse,
    FundraisingActivitySearchResponse,
)
from app.controllers.donee import (
    doneeSearchFundraisingActivityController,
    doneeViewFundraisingActivityController,
    saveFundraisingActivityController,
    searchFavoriteListController,
    doneeSearchCompletedActivitiesController,
    viewCompletedFundraisingActivityController,
    viewFavoriteListController,
    doneeViewCompletedController
)

from app.middleware.access_control import require_roles

require_donee = require_roles("DONEE")

router = APIRouter(prefix="/api/donee", tags=["Donee"])



@router.get("/fundraising_activity/completed", response_model=FundraisingActivitySearchResponse)
def searchCompletedActivity(keyword: str | None = Query(default=None), current_user = Depends(require_donee)):
    if keyword:
        controller = doneeSearchCompletedActivitiesController()
        activities = controller.searchCompletedActivity(keyword)

    else:
        controller = viewCompletedFundraisingActivityController()
        activities = controller.viewCompletedFundraisingActivities()
    
    return {
        "total": len(activities),
        "data": activities,
    }


@router.get("/fundraising_activity/completed/{activity_id}", response_model=FundraisingActivityResponse)
def doneeGetCompletedActivities(activity_id: int, current_user = Depends(require_donee)):
    controller = doneeViewCompletedController()
    result = controller.doneeGetCompletedActivities(activity_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Completed activity not found")

    return result


@router.get("/fundraising_activity/", response_model=FundraisingActivitySearchResponse)
def doneeSearchFundraisingActivity(keyword: str | None = Query(default=None), current_user = Depends(require_donee)):
    controller = doneeSearchFundraisingActivityController()
    activities = controller.doneeSearchFundraisingActivity(keyword)
    return {
        "total": len(activities),
        "data": activities,
    }


@router.get("/fundraising_activity/{activity_id}", response_model=FundraisingActivityResponse)
def doneeViewFundraisingActivity(activity_id: int, current_user = Depends(require_donee)):
    controller = doneeViewFundraisingActivityController()
    result = controller.doneeViewFundraisingActivity(activity_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Activity not found")

    return result


@router.post("/shortlist/", response_model=ShortlistResponse, status_code=201)
def saveFundraisingActivity(payload: ShortlistCreate, current_user = Depends(require_donee)):
    controller = saveFundraisingActivityController()
    result = controller.saveFundraisingActivity(current_user.id, payload.activity_id)

    if result == "activity_not_found":
        raise HTTPException(status_code=404, detail="Activity not found")
    if result == "already_saved":
        raise HTTPException(status_code=400, detail="Activity is already saved to favorites")

    return result


@router.get("/shortlist/", response_model=FavoritesSearchResponse)
def searchFavoriteList(
    keyword: str | None = Query(default=None),
    current_user = Depends(require_donee),
):  
    if keyword:
        
        controller = searchFavoriteListController()
        activities = controller.searchFavoriteList(current_user.id, keyword)
    else:
        controller = viewFavoriteListController()
        activities = controller.viewFavoriteList(current_user.id)
        
    return {
        "total": len(activities),
        "data": activities,
    }