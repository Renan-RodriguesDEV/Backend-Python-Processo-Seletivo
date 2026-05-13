from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.entities.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    location = relationship("Location", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room")

    def __init__(self, name: str, capacity: int, location_id: int):
        self.name = name
        self.capacity = capacity
        self.location_id = location_id
