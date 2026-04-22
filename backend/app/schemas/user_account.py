from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserAccountCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    phone_no: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    dob: Optional[str] = Field(default=None)
    user_profile: str = Field(..., min_length=1, max_length=50)
    status: Optional[str] = Field(default="ACTIVE", pattern="^(ACTIVE|SUSPENDED)$")

class UserAccountUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=100)
    phone_no: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    dob: Optional[str] = Field(default=None)
    user_profile: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(default=None, pattern="^(ACTIVE|SUSPENDED)$")

class UserAccountResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_no: Optional[str]
    address: Optional[str]
    dob: Optional[str]
    status: str
    user_profile_id: int
    name_of_role: Optional[str] = None

    class Config:
        from_attributes = True

class UserAccountSearchResponse(BaseModel):
    total: int
    data: list[UserAccountResponse]