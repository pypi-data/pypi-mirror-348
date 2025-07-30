from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import TripletexResponse


class Activity(BaseModel):
    id: int
    version: int
    url: str
    name: str
    number: Optional[str] = None
    description: Optional[str] = None
    is_inactive: bool = Field(False, alias="isInactive")
    activityType: str

    model_config = ConfigDict(populate_by_name=True)


class ActivityCreate(BaseModel):
    name: str
    number: Optional[str] = None
    description: Optional[str] = None
    activityType: int


class ActivityResponse(TripletexResponse[Activity]):
    pass


class ActivityListCreate(BaseModel):
    """Model for creating multiple activities at once."""

    activities: List[ActivityCreate]

    model_config = ConfigDict(populate_by_name=True)
