from unittest import result

from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.user_account import (
    UserAccountCreate,
    UserAccountUpdate,
    UserAccountResponse,
    UserAccountSearchResponse,
)
from app.controllers.user_account import (
    createUserAccountController,
    viewUserAccountController, 
    updateUserAccountController,
    suspendUserAccountController, 
    searchUserAccountController,
)

router = APIRouter(prefix="/api/user_account", tags=["User Accounts"])

def require_user_admin():
    return None

@router.post("/", response_model=UserAccountResponse, status_code=201)
def create_user_account(
    payload: UserAccountCreate,
    _: None = Depends(require_user_admin)
):
    controller = createUserAccountController()
    result = controller.createUserAccount(
        payload.name,
        payload.email,
        payload.password,
        payload.user_profile,
        payload.phone_no,
        payload.address,
        payload.dob,
        payload.status,
    )

    if result == "duplicate_email":
        raise HTTPException(status_code=400, detail="The email already exists")

    return result

@router.get("/{user_id}", response_model=UserAccountResponse)
def view_user_account(user_id: int,
                      _: None = Depends(require_user_admin),):
    controller = viewUserAccountController()
    result = controller.viewUserAccount(user_id)

    if result is None:
        raise HTTPException(status_code=404, detail="User account not found")

    return result


@router.patch("/{user_id}", response_model=UserAccountResponse)
def update_user_account(
    user_id: int,
    payload: UserAccountUpdate,
    _: None = Depends(require_user_admin),
):
    controller = updateUserAccountController()
    result = controller.updateUserAccount(
        user_id,
        payload.name,
        payload.email,
        payload.password,
        payload.user_profile,
        payload.phone_no,
        payload.address,
        payload.dob,
        payload.status,
    )

    if result == "duplicate_email":
        raise HTTPException(status_code=400, detail="The email already exists")
    
    if result == "invalid_profile":
        raise HTTPException(status_code=400, detail="Invalid user profile")
    
    if result == "not_found":
        raise HTTPException(status_code=404, detail="User account not found")

    return result

@router.patch("/{user_id}/suspend")
def suspend_user_account(user_id: int,
                         _: None = Depends(require_user_admin)):
    
    controller = suspendUserAccountController()
    success = controller.suspendUserAccount(user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User account not found")

    return {"success": True}

@router.get("/", response_model=UserAccountSearchResponse)
def search_user_accounts(
    keyword: str = Query(..., min_length=1, max_length=100),
    _: None = Depends(require_user_admin),
):
    controller = searchUserAccountController()
    accounts = controller.searchUserAccount(keyword)

    return {
        "total": len(accounts),
        "data": accounts
    }