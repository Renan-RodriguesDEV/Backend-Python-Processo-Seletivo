from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from models.entities.base import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(Text, nullable=False)
    rooms = relationship("Room", back_populates="location")

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
