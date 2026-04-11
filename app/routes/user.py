from fastapi import APIRouter
router = APIRouter(prefix="/api/users", tags=["Users"])

from app.middleware.auth import require_user_admin

@router.post("/")
def create_user():
     pass

@router.get("/")
def search_users(): 
     pass

@router.get("/{user_id}")
def get_user(user_id: str): 
     pass

@router.patch("/{user_id}")
def update_user(user_id: str): 
     pass

@router.patch("/{user_id}/suspend")
def suspend_user(user_id: str): 
     pass