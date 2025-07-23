from __future__ import annotations

from datetime import date, datetime
from typing import List
from sqlalchemy.orm import Session

from domain.entities import Booking, Guest, Room, RoomType
from domain.repositories import BookingRepository, GuestRepository, RoomRepository

from .models import BookingModel, GuestModel, RoomModel


class SqlGuestRepository(GuestRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, guest: Guest) -> None:
        self.session.add(
            GuestModel(
                id=guest.id,
                first_name=guest.first_name,
                last_name=guest.last_name,
                date_of_birth=guest.date_of_birth,
            )
        )
        self.session.commit()

    def get(self, guest_id: str) -> Guest | None:
        row = self.session.get(GuestModel, guest_id)
        if row:
            return Guest(
                id=row.id,
                first_name=row.first_name,
                last_name=row.last_name,
                date_of_birth=row.date_of_birth,
            )
        return None


class SqlRoomRepository(RoomRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> List[Room]:
        rows = self.session.query(RoomModel).all()
        return [Room(number=r.number, room_type=RoomType(r.room_type)) for r in rows]

    def get(self, number: str) -> Room | None:
        row = self.session.get(RoomModel, number)
        if row:
            return Room(number=row.number, room_type=RoomType(row.room_type))
        return None


class SqlBookingRepository(BookingRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, booking: Booking) -> None:
        self.session.add(
            BookingModel(
                reference=booking.reference,
                guest_id=booking.guest_id,
                first_name=booking.first_name,
                last_name=booking.last_name,
                date_of_birth=booking.date_of_birth,
                room_type=booking.room_type.value,
                room_number=booking.room_number,
                number_of_guests=booking.number_of_guests,
                check_in=booking.check_in,
                check_out=booking.check_out,
                paid=booking.paid,
                cancelled=booking.cancelled,
                checked_in=booking.checked_in,
                checked_out=booking.checked_out,
                created_at=booking.created_at,
            )
        )
        self.session.commit()

    def get(self, reference: str) -> Booking | None:
        row = self.session.get(BookingModel, reference)
        if row:
            return Booking(
                reference=row.reference,
                guest_id=row.guest_id,
                first_name=row.first_name,
                last_name=row.last_name,
                date_of_birth=row.date_of_birth,
                room_type=RoomType(row.room_type),
                room_number=row.room_number,
                number_of_guests=row.number_of_guests,
                check_in=row.check_in,
                check_out=row.check_out,
                paid=row.paid,
                cancelled=row.cancelled,
                checked_in=row.checked_in,
                checked_out=row.checked_out,
                created_at=row.created_at,
            )
        return None

    def list_for_room(self, room_number: str) -> List[Booking]:
        rows = self.session.query(BookingModel).filter_by(room_number=room_number, cancelled=False).all()
        return [self._to_entity(r) for r in rows]

    def list_for_guest(self, guest_id: str) -> List[Booking]:
        rows = self.session.query(BookingModel).filter_by(guest_id=guest_id).all()
        return [self._to_entity(r) for r in rows]

    def remove(self, reference: str) -> None:
        row = self.session.get(BookingModel, reference)
        if row:
            self.session.delete(row)
            self.session.commit()

    def update(self, booking: Booking) -> None:
        row = self.session.get(BookingModel, booking.reference)
        if not row:
            return
          
        row.guest_id = booking.guest_id
        row.first_name = booking.first_name
        row.last_name = booking.last_name
        row.date_of_birth = booking.date_of_birth
        row.room_type = booking.room_type.value
        row.room_number = booking.room_number

        row.number_of_guests = booking.number_of_guests

        row.check_in = booking.check_in
        row.check_out = booking.check_out
        row.paid = booking.paid
        row.cancelled = booking.cancelled
        row.checked_in = booking.checked_in
        row.checked_out = booking.checked_out
        row.created_at = booking.created_at

        self.session.commit()

    def list_between(self, start: date, end: date) -> List[Booking]:
        rows = self.session.query(BookingModel).filter(
            BookingModel.check_in < end, BookingModel.check_out > start
        ).all()
        return [self._to_entity(r) for r in rows]

    def _to_entity(self, row: BookingModel) -> Booking:
        return Booking(
            reference=row.reference,
            guest_id=row.guest_id,
            first_name=row.first_name,
            last_name=row.last_name,
            date_of_birth=row.date_of_birth,
            room_type=RoomType(row.room_type),
            room_number=row.room_number,
            number_of_guests=row.number_of_guests,
            check_in=row.check_in,
            check_out=row.check_out,
            paid=row.paid,
            cancelled=row.cancelled,
            checked_in=row.checked_in,
            checked_out=row.checked_out,
            created_at=row.created_at,

        )
