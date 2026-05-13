import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from config.db import get_db, get_engine


@pytest.mark.connect
def test_connect():
    assert isinstance(get_db(), Session)


@pytest.mark.rooms
def test_rooms():
    with get_engine().connect() as conn:
        with conn.begin():
            result = conn.execute(text("SELECT * FROM rooms"))
            print(result.fetchall())
        assert result is not None


@pytest.mark.reservations
def test_reservations():
    with get_engine().connect() as conn:
        with conn.begin():
            result = conn.execute(text("SELECT * FROM reservations"))
            print(result.fetchall())
        assert result is not None


@pytest.mark.locations
def test_locations():
    with get_engine().connect() as conn:
        with conn.begin():
            result = conn.execute(text("SELECT * FROM locations"))
            print(result.fetchall())
        assert result is not None
