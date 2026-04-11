from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db

from app.models.user_profile import UserProfile
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserProfileSearchResponse
)
from app.controllers import (
    createUserProfile, 
    getUserProfileByID, 
    updateUserProfile, 
    suspendUserProfile, 
    searchUserProfile
)


router = APIRouter(prefix="/api/user_profile", tags=["User Profiles"])

def require_user_admin():
    return None

@router.post("/", status_code=201)
def create_user_profile(payload: UserProfileCreate, db: Session = Depends(get_db)):
    success = createUserProfile(payload.name_of_role, payload.description, db)
    return {"success": success}

@router.get("/{profile_id}", response_model=UserProfileResponse)
def get_user_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_user_admin),
):
    return getUserProfileByID(profile_id, db)

@router.patch("/{profile_id}", response_model=UserProfileResponse)
def update_user_profile(
    profile_id: int,
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_user_admin),
):
    return updateUserProfile(profile_id, payload.name_of_role, payload.description, db)

@router.patch("/{profile_id}/suspend")
def suspend_user_profile(profile_id: int, db: Session = Depends(get_db)):
    success = suspendUserProfile(profile_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User profile not found")
    return {"success": True}

@router.get("/",response_model=UserProfileSearchResponse)
def search_user_profiles(
    keyword: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: None = Depends(require_user_admin),
):
    return searchUserProfile(keyword, db)