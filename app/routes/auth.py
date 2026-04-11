from fastapi import APIRouter
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login")
def login(): 
    pass

@router.post("/logout")
def logout(): 
    pass