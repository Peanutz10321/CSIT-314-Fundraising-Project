from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ShortlistCreate(BaseModel):
    donee_id: int
    activity_id: int


class ShortlistResponse(BaseModel):
    id: int
    donee_id: int
    activity_id: int
    date_saved: datetime

    class Config:
        from_attributes = True

from app.schemas.fundraising_activity import FundraisingActivityResponse


class FavoritesSearchResponse(BaseModel):
    total: int
    data: list[FundraisingActivityResponse]