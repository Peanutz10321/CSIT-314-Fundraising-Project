from pydantic import BaseModel, Field
from typing import Optional


class UserProfileCreate(BaseModel):
    name_of_role: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    status: Optional[str] = Field(default="ACTIVE", pattern="^(ACTIVE|SUSPENDED)$")

class UserProfileUpdate(BaseModel):
    name_of_role: Optional[str] = Field(default=None, min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    status: Optional[str] = Field(default=None, pattern="^(ACTIVE|SUSPENDED)$")

class UserProfileResponse(BaseModel):
    id: int
    name_of_role: str
    description: Optional[str]
    status: str

    class Config:
        from_attributes = True

class UserProfileSearchResponse(BaseModel):
    total: int
    data: list[UserProfileResponse]