from fastapi import APIRouter, HTTPException, Query
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
    doneeViewCompletedController,
)

router = APIRouter(prefix="/api/donee", tags=["Donee"])



@router.get("/fundraising_activity/completed", response_model=FundraisingActivitySearchResponse)
def donee_search_completed_activities(keyword: str | None = Query(default=None)):
    controller = doneeSearchCompletedActivitiesController()
    activities = controller.searchCompletedActivity(keyword)
    return {
        "total": len(activities),
        "data": activities,
    }


@router.get("/fundraising_activity/completed/{activity_id}", response_model=FundraisingActivityResponse)
def donee_view_completed_activity(activity_id: int):
    controller = doneeViewCompletedController()
    result = controller.doneeGetCompletedActivities(activity_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Completed activity not found")

    return result


@router.get("/fundraising_activity/", response_model=FundraisingActivitySearchResponse)
def donee_search_activities(keyword: str | None = Query(default=None)):
    controller = doneeSearchFundraisingActivityController()
    activities = controller.searchFundraisingActivity(keyword)
    return {
        "total": len(activities),
        "data": activities,
    }


@router.get("/fundraising_activity/{activity_id}", response_model=FundraisingActivityResponse)
def donee_view_activity(activity_id: int):
    controller = doneeViewFundraisingActivityController()
    result = controller.doneeViewFundraisingActivity(activity_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Activity not found")

    return result


@router.post("/shortlist/", response_model=ShortlistResponse, status_code=201)
def save_activity(payload: ShortlistCreate):
    controller = saveFundraisingActivityController()
    result = controller.saveFundraisingActivity(payload.donee_id, payload.activity_id)

    if result == "activity_not_found":
        raise HTTPException(status_code=404, detail="Activity not found")
    if result == "already_saved":
        raise HTTPException(status_code=400, detail="Activity is already saved to favorites")

    return result


@router.get("/shortlist/", response_model=FavoritesSearchResponse)
def get_favorites(
    donee_id: int = Query(...),
    keyword: str | None = Query(default=None),
):
    controller = searchFavoriteListController()
    activities = controller.searchFavoriteList(donee_id, keyword)
    return {
        "total": len(activities),
        "data": activities,
    }