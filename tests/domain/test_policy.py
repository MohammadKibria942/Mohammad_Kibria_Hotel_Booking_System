from datetime import date, timedelta

import pytest

from src.domain.entities import Booking, Guest, RoomType
from src.domain.services import BookingPolicy


def test_booking_policy_allows_valid_booking():
    policy = BookingPolicy()
    guest = Guest(
        id="g1",
        first_name="Bob",
        last_name="Jones",
        date_of_birth=date.today() - timedelta(days=20 * 365),
    )
    booking = Booking(
        reference="r1",
        guest_id="g1",
        first_name=guest.first_name,
        last_name=guest.last_name,
        date_of_birth=guest.date_of_birth,
        room_type=RoomType.STANDARD,
        room_number="101",
        number_of_guests=1,
        check_in=date.today() + timedelta(days=2),
        check_out=date.today() + timedelta(days=3),
    )
    policy.validate_new_booking(guest, [], booking)


def test_booking_policy_rejects_underage():
    policy = BookingPolicy()
    guest = Guest(
        id="g1",
        first_name="Bob",
        last_name="Jones",
        date_of_birth=date.today() - timedelta(days=17 * 365),
    )
    booking = Booking(
        reference="r1",
        guest_id="g1",
        first_name=guest.first_name,
        last_name=guest.last_name,
        date_of_birth=guest.date_of_birth,
        room_type=RoomType.STANDARD,
        room_number="101",
        number_of_guests=1,
        check_in=date.today() + timedelta(days=2),
        check_out=date.today() + timedelta(days=3),
    )
    with pytest.raises(ValueError):
        policy.validate_new_booking(guest, [], booking)


def test_booking_policy_rejects_too_many_guests():
    policy = BookingPolicy()
    guest = Guest(
        id="g1",
        first_name="Bob",
        last_name="Jones",
        date_of_birth=date.today() - timedelta(days=20 * 365),
    )
    booking = Booking(
        reference="r1",
        guest_id="g1",
        first_name=guest.first_name,
        last_name=guest.last_name,
        date_of_birth=guest.date_of_birth,
        room_type=RoomType.STANDARD,
        room_number="101",
        number_of_guests=5,
        check_in=date.today() + timedelta(days=2),
        check_out=date.today() + timedelta(days=3),
    )
    with pytest.raises(ValueError):
        policy.validate_new_booking(guest, [], booking)
