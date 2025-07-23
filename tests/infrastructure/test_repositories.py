from datetime import date, timedelta

from infrastructure.db import get_engine, create_session, init_db
from infrastructure.repositories import (
    SqlBookingRepository,
    SqlGuestRepository,
    SqlRoomRepository,
)
from infrastructure.models import Base
from domain.entities import Guest


def setup_function() -> None:
    engine = get_engine("sqlite:///./test.db")
    init_db(engine)
    _ = create_session(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def create_repos():
    engine = get_engine("sqlite:///./test.db")
    session = create_session(engine)
    return (
        SqlBookingRepository(session),
        SqlGuestRepository(session),
        SqlRoomRepository(session),
        session,
    )


def test_guest_repository():
    booking_repo, guest_repo, room_repo, session = create_repos()
    guest = Guest(
        id="g1",
        first_name="Alice",
        last_name="Smith",
        date_of_birth=date.today() - timedelta(days=30 * 365),
    )
    guest_repo.add(guest)
    fetched = guest_repo.get("g1")
    assert fetched is not None and fetched.first_name == "Alice"
