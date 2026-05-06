from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FundraisingCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class FundraisingCategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class FundraisingCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    date_created: datetime
    activity_count: int

    class Config:
        from_attributes = True


class FundraisingCategorySearchResponse(BaseModel):
    total: int
    data: list[FundraisingCategoryResponse]
