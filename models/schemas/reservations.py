import datetime
from typing import Optional

from pydantic import BaseModel

from models.schemas.rooms import RoomResponse


class ReservationRequest(BaseModel):
    room_id: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    responsible: str
    coffee: bool = False
    people_count: Optional[int] = None
    description: Optional[str] = None


class ReservationRequestUpdate(BaseModel):
    room_id: Optional[int] = None
    start_datetime: Optional[datetime.datetime] = None
    end_datetime: Optional[datetime.datetime] = None
    responsible: Optional[str] = None
    coffee: Optional[bool] = False
    people_count: Optional[int] = None
    description: Optional[str] = None


class ReservationResponse(ReservationRequest):
    id: int
    created_at: datetime.datetime
    room: RoomResponse
