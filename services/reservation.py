import datetime

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

    Detecta conflito quando: existing.start <= new.end AND existing.end >= new.start
    """
    query = session.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.start_datetime
        <= end,  # Reserva existente começa antes ou no mesmo momento do término
        Reservation.end_datetime
        >= start,  # Reserva existente termina depois ou no mesmo momento do início
    )
    if exclude_id:
        query = query.filter(Reservation.id != exclude_id)
    return query.first() is not None
