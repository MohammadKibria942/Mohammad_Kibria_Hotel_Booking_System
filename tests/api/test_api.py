from datetime import date, timedelta

from fastapi.testclient import TestClient

from src.api.main import app, session
from src.infrastructure.models import GuestModel, RoomModel, BookingModel

client = TestClient(app)


def test_create_and_get_booking():
    session.query(BookingModel).delete()
    session.query(GuestModel).delete()
    session.query(RoomModel).delete()
    session.commit()

    session.add(
        GuestModel(
            id="g1",
            first_name="Alice",
            last_name="Smith",
            date_of_birth=date.today() - timedelta(days=30 * 365),
        )
    )
    session.add(RoomModel(number="101", room_type="standard"))
    session.commit()

    payload = {
        "guest_id": "g1",
        "first_name": "Alice",
        "last_name": "Smith",
        "date_of_birth": str(date.today() - timedelta(days=30 * 365)),
        "room_type": "standard",
        "room_number": "101",
        "number_of_guests": 1,
        "check_in": str(date.today() + timedelta(days=1)),
        "check_out": str(date.today() + timedelta(days=2)),
        "cancelled": False,
        "checked_in": False,
        "checked_out": False,
        "paid": True,
    }
    resp = client.post("/bookings", json=payload)
    assert resp.status_code == 200
    ref = resp.json()["reference"]

    resp = client.get(f"/bookings/{ref}")
    assert resp.status_code == 200
    assert resp.json()["reference"] == ref


def clear_db():
    session.query(BookingModel).delete()
    session.query(GuestModel).delete()
    session.query(RoomModel).delete()
    session.commit()


def test_cancel_booking():
    clear_db()
    session.add(
        GuestModel(
            id="g1",
            first_name="Alice",
            last_name="Smith",
            date_of_birth=date.today() - timedelta(days=30 * 365),
        )
    )
    session.add(RoomModel(number="101", room_type="standard"))
    session.commit()

    payload = {
        "guest_id": "g1",
        "first_name": "Alice",
        "last_name": "Smith",
        "date_of_birth": str(date.today() - timedelta(days=30 * 365)),
        "room_type": "standard",
        "room_number": "101",
        "number_of_guests": 1,

        "check_in": str(date.today() + timedelta(days=1)),
        "check_out": str(date.today() + timedelta(days=2)),
        "cancelled": False,
        "checked_in": False,
        "checked_out": False,
        "paid": True,
    }
    ref = client.post("/bookings", json=payload).json()["reference"]
    resp = client.delete(f"/bookings/{ref}")
    assert resp.status_code == 200
    resp = client.get(f"/bookings/{ref}")
    assert resp.status_code == 404


def test_room_availability():
    clear_db()
    session.add(
        GuestModel(
            id="g1",
            first_name="Bob",
            last_name="Brown",
            date_of_birth=date.today() - timedelta(days=30 * 365),
        )
    )
    session.add_all([
        RoomModel(number="101", room_type="standard"),
        RoomModel(number="102", room_type="standard"),
    ])
    session.commit()

    payload = {
        "guest_id": "g1",
        "first_name": "Bob",
        "last_name": "Brown",
        "date_of_birth": str(date.today() - timedelta(days=30 * 365)),
        "room_type": "standard",
        "room_number": "101",

        "number_of_guests": 2,

        "check_in": str(date.today() + timedelta(days=1)),
        "check_out": str(date.today() + timedelta(days=3)),
        "cancelled": False,
        "checked_in": False,
        "checked_out": False,
        "paid": True,
    }
    client.post("/bookings", json=payload)

    start = str(date.today() + timedelta(days=1))
    end = str(date.today() + timedelta(days=2))
    resp = client.get(f"/rooms/availability?start={start}&end={end}")
    assert resp.status_code == 200
    rooms = {r["number"] for r in resp.json()}
    assert "102" in rooms and "101" not in rooms


def test_check_in_and_out():
    clear_db()
    session.add(
        GuestModel(
            id="g1",
            first_name="Eve",
            last_name="Adams",
            date_of_birth=date.today() - timedelta(days=30 * 365),
        )
    )
    session.add(RoomModel(number="101", room_type="standard"))
    session.commit()

    payload = {
        "guest_id": "g1",
        "first_name": "Eve",
        "last_name": "Adams",
        "date_of_birth": str(date.today() - timedelta(days=30 * 365)),
        "room_type": "standard",
        "room_number": "101",
        "number_of_guests": 1,

        "check_in": str(date.today() + timedelta(days=1)),
        "check_out": str(date.today() + timedelta(days=2)),
        "cancelled": False,
        "checked_in": False,
        "checked_out": False,
        "paid": True,
    }
    ref = client.post("/bookings", json=payload).json()["reference"]
    resp = client.post(f"/bookings/{ref}/check-in")
    assert resp.status_code == 200
    assert resp.json()["checked_in"] is True
    resp = client.post(f"/bookings/{ref}/check-out")
    assert resp.status_code == 200
    assert resp.json()["checked_out"] is True


def test_guest_history_and_register():
    clear_db()
    resp = client.post(
        "/guests",
        json={
            "id": "g2",
            "first_name": "Zoe",
            "last_name": "Zeta",
            "date_of_birth": str(date.today() - timedelta(days=25 * 365)),
        },
    )
    assert resp.status_code == 200
    session.add(RoomModel(number="101", room_type="standard"))
    session.commit()

    payload = {
        "guest_id": "g2",
        "first_name": "Zoe",
        "last_name": "Zeta",
        "date_of_birth": str(date.today() - timedelta(days=25 * 365)),
        "room_type": "standard",
        "room_number": "101",

        "number_of_guests": 1,

        "check_in": str(date.today() + timedelta(days=1)),
        "check_out": str(date.today() + timedelta(days=2)),
        "cancelled": False,
        "checked_in": False,
        "checked_out": False,
        "paid": True,
    }
    client.post("/bookings", json=payload)
    resp = client.get("/guests/g2/bookings")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

