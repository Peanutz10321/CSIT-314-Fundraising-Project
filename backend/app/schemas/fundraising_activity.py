from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FundraisingActivityCreate(BaseModel):
    fundraiser_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    currency: str = Field(..., min_length=1, max_length=10)
    goal_amount: float = Field(..., gt=0)
    category: str = Field(default=None, max_length=100)
    location: Optional[str] = Field(default=None, max_length=255)
    beneficiaryName: Optional[str] = Field(default=None, max_length=255)
    fundraiserName: Optional[str] = Field(default=None, max_length=255)
    deadline: str


class FundraisingActivityUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    currency: Optional[str] = Field(default=None, max_length=10)
    goal_amount: Optional[float] = Field(default=None, gt=0)
    category: str = Field(default=None, max_length=100)
    location: Optional[str] = Field(default=None, max_length=255)
    beneficiaryName: Optional[str] = Field(default=None, max_length=255)
    fundraiserName: Optional[str] = Field(default=None, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    deadline: Optional[str] = None


class FundraisingActivityResponse(BaseModel):
    id: int
    fundraiser_id: int
    title: str
    description: Optional[str]
    currency: str
    goal_amount: float
    current_amount: float
    category: str
    location: Optional[str]
    beneficiaryName: Optional[str]
    fundraiserName: Optional[str]
    deadline: Optional[str]
    status: str
    view_count: int
    shortlist_count: int
    date_created: datetime

    class Config:
        from_attributes = True


class FundraisingActivitySearchResponse(BaseModel):
    total: int
    data: list[FundraisingActivityResponse]