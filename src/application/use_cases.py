from __future__ import annotations

from dataclasses import dataclass
import uuid
from datetime import date, datetime
from typing import List

from domain.entities import Booking, Guest, RoomType
from domain.repositories import BookingRepository, GuestRepository, RoomRepository
from domain.services import BookingPolicy


@dataclass
class CreateBookingRequest:
    guest_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    room_type: RoomType
    room_number: str
    number_of_guests: int

    check_in: date
    check_out: date
    cancelled: bool = False
    checked_in: bool = False
    checked_out: bool = False
    paid: bool = False


class BookingService:
    def __init__(
        self,
        booking_repo: BookingRepository,
        guest_repo: GuestRepository,
        room_repo: RoomRepository,
        policy: BookingPolicy,
    ) -> None:
        self.booking_repo = booking_repo
        self.guest_repo = guest_repo
        self.room_repo = room_repo
        self.policy = policy

    def create_booking(self, req: CreateBookingRequest) -> Booking:
        guest = self.guest_repo.get(req.guest_id)
        if guest is None:
            guest = Guest(
                id=req.guest_id,
                first_name=req.first_name,
                last_name=req.last_name,
                date_of_birth=req.date_of_birth,
            )
            self.guest_repo.add(guest)
        else:
            if (
                guest.first_name != req.first_name
                or guest.last_name != req.last_name
                or guest.date_of_birth != req.date_of_birth
            ):
                raise ValueError("Guest details mismatch")

        room = self.room_repo.get(req.room_number)
        if room is None:
            raise ValueError("Room not found")
        if room.room_type != req.room_type:
            raise ValueError("Room type mismatch")
        existing = self.booking_repo.list_for_room(req.room_number)
        booking = Booking(
            reference=str(uuid.uuid4())[:10],
            guest_id=req.guest_id,
            first_name=req.first_name,
            last_name=req.last_name,
            date_of_birth=req.date_of_birth,
            room_type=req.room_type,
            room_number=req.room_number,
            number_of_guests=req.number_of_guests,
            check_in=req.check_in,
            check_out=req.check_out,
            cancelled=req.cancelled,
            checked_in=req.checked_in,
            checked_out=req.checked_out,
            paid=req.paid,
            created_at=datetime.utcnow(),
        )
        self.policy.validate_new_booking(guest, existing, booking)
        self.booking_repo.add(booking)
        return booking

    def get_booking(self, reference: str) -> Booking | None:
        return self.booking_repo.get(reference)

    def list_guest_bookings(self, guest_id: str) -> List[Booking]:
        return self.booking_repo.list_for_guest(guest_id)

    def cancel_booking(self, reference: str) -> None:
        booking = self.booking_repo.get(reference)
        if not booking:
            raise ValueError("Booking not found")
        self.booking_repo.remove(reference)

    def check_in_booking(self, reference: str) -> Booking:
        booking = self.booking_repo.get(reference)
        if not booking:
            raise ValueError("Booking not found")
        booking.checked_in = True
        self.booking_repo.update(booking)
        return booking

    def check_out_booking(self, reference: str) -> Booking:
        booking = self.booking_repo.get(reference)
        if not booking:
            raise ValueError("Booking not found")
        booking.checked_out = True
        self.booking_repo.update(booking)
        return booking

    def list_rooms(self):
        return self.room_repo.list_all()

    def available_rooms(self, start: date, end: date):
        rooms = self.room_repo.list_all()
        bookings = self.booking_repo.list_between(start, end)
        booked = {b.room_number for b in bookings if not b.cancelled}
        return [r for r in rooms if r.number not in booked]

    def create_guest(
        self, guest_id: str, first_name: str, last_name: str, date_of_birth: date
    ) -> Guest:
        if self.guest_repo.get(guest_id):
            raise ValueError("Guest already exists")
        guest = Guest(
            id=guest_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        self.guest_repo.add(guest)
        return guest
