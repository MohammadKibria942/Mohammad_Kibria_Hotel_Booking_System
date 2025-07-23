from datetime import date, timedelta

from application.use_cases import BookingService, CreateBookingRequest
from domain.entities import Guest, RoomType
from domain.services import BookingPolicy
from infrastructure.models import RoomModel
from infrastructure.repositories import SqlBookingRepository, SqlGuestRepository, SqlRoomRepository
from infrastructure.db import get_engine, create_session, init_db
from infrastructure.models import Base


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


def test_create_booking(tmp_path):
    booking_repo, guest_repo, room_repo, session = create_repos()
    guest = Guest(
        id="g1",
        first_name="Alice",
        last_name="Smith",
        date_of_birth=date.today() - timedelta(days=30 * 365),
    )
    guest_repo.add(guest)
    room_repo.session.add(RoomModel(number="101", room_type="standard"))
    session.commit()

    service = BookingService(
        booking_repo, guest_repo, room_repo, BookingPolicy()
    )

    req = CreateBookingRequest(
        guest_id="g1",
        first_name="Alice",
        last_name="Smith",
        date_of_birth=date.today() - timedelta(days=30 * 365),
        room_type=RoomType.STANDARD,
        room_number="101",
        number_of_guests=1,
        check_in=date.today() + timedelta(days=1),
        check_out=date.today() + timedelta(days=2),
        paid=True,
    )

    booking = service.create_booking(req)
    assert booking.reference
    fetched = service.get_booking(booking.reference)
    assert fetched is not None
