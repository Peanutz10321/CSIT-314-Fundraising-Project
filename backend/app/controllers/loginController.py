from sqlalchemy.orm import Session
from app.entities.login_code import LoginCode
from app.middleware.auth import create_access_token

def validateCredentials(db: Session, email: str, password: str):
    code = LoginCode(db)
    result = code.validateCredentials(email, password)

    if not result["success"]:
        return result

    user = result["user"]
    token = create_access_token({"sub": str(user.id)})

    return {
        "success": True,
        "reason": None,
        "token": token,
        "role": user.user_profile.name_of_role if user.user_profile else None,
    }