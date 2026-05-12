import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


SessionLocal = None
engine: Engine = None


def get_engine():
    global engine
    if not engine:
        engine = create_engine(
            DB_URL,
            pool_recycle=3600,
            echo=True if os.getenv("DEBUG") == "TRUE" else False,
        )
    return engine


def get_session():
    global SessionLocal
    if not SessionLocal:
        SessionLocal = sessionmaker(bind=get_engine())
    return SessionLocal()


def get_db():
    db = get_session()
    try:
        yield db
    except Exception as e:
        # logging.error(f"Database error: {e}")
        db.rollback()
        raise e
    finally:
        db.close()
