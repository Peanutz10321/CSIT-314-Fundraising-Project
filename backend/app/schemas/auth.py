from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

class LoginResponse(BaseModel):
    token: str
    role: str

class LogoutResponse(BaseModel):
    message: str