from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.access_control import require_roles

from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserProfileSearchResponse
)
from app.controllers.user_profile import (
    createUserProfileController,
    viewUserProfileController,
    updateUserProfileController,
    suspendUserProfileController,
    searchUserProfileController
)

router = APIRouter(prefix="/api/user_profile", tags=["User Profiles"])

require_user_admin = require_roles("USER_ADMIN")


@router.post("/", response_model=UserProfileResponse, status_code=201)
def create_user_profile(
    payload: UserProfileCreate,
    _: None = Depends(require_user_admin)
):
    controller = createUserProfileController()
    result = controller.createUserProfile(payload.name_of_role, payload.description)

    if result == "duplicate_name":
        raise HTTPException(status_code=400, detail="The name already exists")

    return result


@router.get("/{profile_id}", response_model=UserProfileResponse)
def get_user_profile(
    profile_id: int,
    _: None = Depends(require_user_admin)
):
    controller = viewUserProfileController()
    result = controller.getUserProfileByID(profile_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="User profile not found")

    return result


@router.patch("/{profile_id}", response_model=UserProfileResponse)
def update_user_profile(
    profile_id: int,
    payload: UserProfileUpdate,
    _: None = Depends(require_user_admin)
):
    controller = updateUserProfileController()
    result = controller.updateUserProfile(
        profile_id,
        payload.name_of_role,
        payload.description,
    )

    if result == "not_found":
        raise HTTPException(status_code=404, detail="User profile not found")
    
    if result == "duplicate_name":
        raise HTTPException(status_code=400, detail="The user profile name already exists")

    return result


@router.patch("/{profile_id}/suspend")
def suspend_user_profile(
    profile_id: int,
    _: None = Depends(require_user_admin)
):
    controller = suspendUserProfileController()
    success = controller.suspendUserProfile(profile_id)

    if not success:
        raise HTTPException(status_code=404, detail="User profile not found")

    return {"success": True}


@router.get("/", response_model=UserProfileSearchResponse)
def search_user_profiles(
    keyword: str | None = Query(default=None),
    _: None = Depends(require_user_admin)
):
    controller = searchUserProfileController()
    profiles = controller.searchUserProfile(keyword)

    return {
        "total": len(profiles),
        "data": profiles
    }