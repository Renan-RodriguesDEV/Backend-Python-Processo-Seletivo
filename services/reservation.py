import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from models.entities.reservations import Reservation


def check_time_conflict(
    room_id: int,
    start: datetime.datetime,
    end: datetime.datetime,
    session: Session,
    exclude_id: int = None,
) -> bool:
    """Verifica se há reserva sobreposta na mesma sala.

    Detecta conflito quando existe uma reserva com intervalo que se sobrepõe ao novo.
    A condição correta é:
        existing.start < new.end AND existing.end > new.start
    """

    query = session.query(Reservation).filter(
        Reservation.room_id == room_id,
        and_(
            Reservation.start_datetime < end,
            Reservation.end_datetime > start,
        ),
    )
    if exclude_id:
        query = query.filter(Reservation.id != exclude_id)
    return query.first() is not None
