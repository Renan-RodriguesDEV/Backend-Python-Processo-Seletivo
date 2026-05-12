import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from models.entities.base import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    responsible = Column(String, nullable=False)
    coffee = Column(Boolean, default=False)
    people_count = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    room = relationship("Room", back_populates="reservations")

    def __init__(
        self,
        room_id: int,
        start_datetime: datetime.datetime,
        end_datetime: datetime.datetime,
        responsible: str,
        coffee: bool = False,
        people_count: int = None,
        description: str = None,
    ):
        self.room_id = room_id
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.responsible = responsible
        self.coffee = coffee
        self.people_count = people_count
        self.description = description
