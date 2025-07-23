from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base, RoomModel


def get_engine(url: str = "sqlite:///./hotel.db"):
    return create_engine(url, echo=False)


def create_session(engine) -> Session:
    return sessionmaker(bind=engine)()


def init_db(engine) -> None:
    """Create fresh tables for the configured engine."""
    # Recreate the schema so database columns always match the models.
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # Populate a default set of rooms so the API works on a fresh install
    session = create_session(engine)
    if not session.query(RoomModel).count():
        rooms: list[RoomModel] = []
        for i in range(100):
            number = str(101 + i)
            if i < 50:
                room_type = "standard"
            elif i < 80:
                room_type = "deluxe"
            else:
                room_type = "suite"
            rooms.append(RoomModel(number=number, room_type=room_type))
        session.add_all(rooms)
        session.commit()
    session.close()
