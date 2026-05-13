"""
POST /reservations - criar nova reserva
GET /reservations - listar todas
GET /reservations/{id} - detalhe
PUT /reservations/{id} - editar
DELETE /reservations/{id} - deletar único
DELETE /reservations/batch - deletar múltiplas (opcional)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.db import get_db
from config.logger import logger
from models.entities.reservations import Reservation
from models.schemas.reservations import (
    EntityIds,
    ReservationRequest,
    ReservationRequestUpdate,
    ReservationResponse,
)
from services.reservation import check_time_conflict

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post(
    "/",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    description="Cria uma nova reserva. Forneça os detalhes da reserva no corpo da requisição.",
)
def create(
    reservation: ReservationRequest,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    if reservation.end_datetime <= reservation.start_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_datetime must be after start_datetime.",
        )

    if check_time_conflict(
        room_id=reservation.room_id,
        start=reservation.start_datetime,
        end=reservation.end_datetime,
        session=session,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time conflict found for this reservation.",
        )
    logger.debug(f"Creating reservation with data: {reservation}")
    db_reservation = Reservation(**reservation.model_dump())
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation


@router.put(
    "/{id}",
    response_model=ReservationResponse,
    status_code=status.HTTP_200_OK,
    description="Atualiza os detalhes de uma reserva existente. Forneça apenas os campos que deseja atualizar.",
)
def update(
    id: int,
    reservation: ReservationRequestUpdate,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    logger.debug(f"Updating reservation with data: {reservation}")
    db_reservation = session.query(Reservation).filter(Reservation.id == id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found"
        )
    new_start = reservation.start_datetime or db_reservation.start_datetime
    new_end = reservation.end_datetime or db_reservation.end_datetime

    if new_end <= new_start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_datetime must be after start_datetime.",
        )

    if check_time_conflict(
        room_id=reservation.room_id or db_reservation.room_id,
        start=new_start,
        end=new_end,
        session=session,
        exclude_id=id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time conflict found for this reservation.",
        )

    for k, v in reservation.model_dump().items():
        if v is not None:
            setattr(db_reservation, k, v)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation


@router.get(
    "/",
    response_model=list[ReservationResponse],
    status_code=status.HTTP_200_OK,
    description="Lista todas as reservas.",
)
def list_all(
    session: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    return session.query(Reservation).all()


@router.get(
    "/{id}",
    response_model=ReservationResponse,
    status_code=status.HTTP_200_OK,
    description="Lista uma reserva especifica.",
)
def list_one(
    id: int,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    reservation = session.query(Reservation).filter(Reservation.id == id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found"
        )
    logger.debug(f"Fetching reservation with data: {reservation}")
    return reservation


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Deleta uma reserva especifica.",
)
def delete_one(
    id: int,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    reservation = session.query(Reservation).filter(Reservation.id == id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found"
        )
    session.delete(reservation)
    session.commit()
    logger.debug(f"Deleting reservation with data: {reservation}")
    return


@router.delete(
    "/batch/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Deleta múltiplas reservas por IDs.",
)
def delete_all(
    entity_ids: EntityIds,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    reservations = (
        session.query(Reservation).where(Reservation.id.in_(entity_ids.ids)).all()
    )
    logger.debug(f"Len of IDs: {len(reservations)}")
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservations not found"
        )
    for reservation in reservations:
        session.delete(reservation)
    session.commit()
    logger.debug(f"Deleting all reservations with data: {reservations}")
    return
