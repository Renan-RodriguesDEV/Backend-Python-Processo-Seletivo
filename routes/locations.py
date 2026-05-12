"""
GET /locations - listar locais
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from config.db import get_db
from models.entities.locations import Location
from models.schemas.locations import LocationRequest, LocationResponse

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post(
    "/",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED,
    description="Cria um novo local. Forneça os detalhes do local no corpo da requisição. (rota feita para facilitar a criação de locais, já que não há uma interface de administração)",
)
def create(
    location: LocationRequest,
    session: Session = Depends(get_db),
    # current_user: str = Depends(get_current_user),
):
    db_location = Location(**location.model_dump())
    session.add(db_location)
    session.commit()
    session.refresh(db_location)
    return db_location


@router.get(
    "/",
    response_model=list[LocationResponse],
    description="Lista todos os locais.",
    status_code=status.HTTP_200_OK,
)
def list_all(
    session: Session = Depends(get_db),
    # current_user: str = Depends(get_current_user),
):
    return session.query(Location).all()
