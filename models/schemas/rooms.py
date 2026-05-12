from typing import Optional

from pydantic import BaseModel

from models.schemas.locations import LocationResponse


class RoomRequest(BaseModel):
    name: str
    location_id: int
    capacity: int


class RoomRequestUpdate(BaseModel):
    name: Optional[str] = None
    location_id: Optional[int] = None
    capacity: Optional[int] = None


class RoomResponse(RoomRequest):
    id: int
    location: LocationResponse
