from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserAccountCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    user_profile_id: int


class UserAccountResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    status: str
    user_profile_id: int

    class Config:
        from_attributes = True