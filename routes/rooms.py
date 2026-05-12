"""
GET /rooms - listar salas
POST /rooms - criar sala
PUT /rooms/{id} - editar sala (se necessário)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.db import get_db
from models.entities.rooms import Room
from models.schemas.rooms import RoomRequest, RoomRequestUpdate, RoomResponse

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RoomResponse,
    description="Cria uma nova sala. Forneça os detalhes da sala no corpo da requisição.",
)
def create(
    room: RoomRequest,
    session: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),
):
    room_db = Room(**room.model_dump())
    session.add(room_db)
    session.commit()
    session.refresh(room_db)
    return room_db


@router.get("/", response_model=list[RoomResponse], description="Lista todas as salas.")
def list_all(
    session: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),
):
    return session.query(Room).all()


@router.put(
    "/{id}",
    description="Atualiza os detalhes de uma sala existente. Forneça apenas os campos que deseja atualizar.",
    response_model=RoomResponse,
)
def update(
    id: int,
    room: RoomRequestUpdate,
    session: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),
):
    room_db = session.query(Room).filter(Room.id == id).first()
    if not room_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )
    for k, v in room.model_dump().items():
        if v is not None:
            setattr(room_db, k, v)
    session.commit()
    session.refresh(room_db)
    return room_db
