from pydantic import BaseModel


class LocationRequest(BaseModel):
    name: str
    address: str


class LocationResponse(LocationRequest):
    id: int
