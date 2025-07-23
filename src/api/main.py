from __future__ import annotations

from datetime import date, datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from domain.services import BookingPolicy
from domain.entities import RoomType
from infrastructure.db import create_session, get_engine, init_db
from infrastructure.repositories import (
    SqlBookingRepository,
    SqlGuestRepository,
    SqlRoomRepository,
)
from application.use_cases import BookingService, CreateBookingRequest

app = FastAPI()

engine = get_engine()
init_db(engine)
session = create_session(engine)
booking_service = BookingService(
    SqlBookingRepository(session),
    SqlGuestRepository(session),
    SqlRoomRepository(session),
    BookingPolicy(),
)


class BookingIn(BaseModel):
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


class BookingOut(BaseModel):
    reference: str
    guest_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    room_type: RoomType
    room_number: str
    number_of_guests: int
    check_in: date
    check_out: date
    cancelled: bool
    checked_in: bool
    checked_out: bool
    paid: bool
    created_at: datetime


class RoomOut(BaseModel):
    number: str
    room_type: RoomType


class GuestIn(BaseModel):
    id: str
    first_name: str
    last_name: str
    date_of_birth: date


class GuestOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    date_of_birth: date


@app.post("/bookings", response_model=BookingOut)
def create_booking(data: BookingIn):
    try:
        booking = booking_service.create_booking(
            CreateBookingRequest(
                guest_id=data.guest_id,
                first_name=data.first_name,
                last_name=data.last_name,
                date_of_birth=data.date_of_birth,
                room_type=data.room_type,
                room_number=data.room_number,
                number_of_guests=data.number_of_guests,
                check_in=data.check_in,
                check_out=data.check_out,
                cancelled=data.cancelled,
                checked_in=data.checked_in,
                checked_out=data.checked_out,
                paid=data.paid,
            )
        )
        return BookingOut(**booking.__dict__)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/bookings/{reference}", response_model=BookingOut)
def get_booking(reference: str):
    booking = booking_service.get_booking(reference)
    if not booking:
        raise HTTPException(status_code=404, detail="Not found")
    return BookingOut(**booking.__dict__)


@app.delete("/bookings/{reference}")
def cancel_booking(reference: str):
    try:
        booking_service.cancel_booking(reference)
        return {"status": "cancelled"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")


@app.get("/rooms", response_model=list[RoomOut])
def list_rooms():
    rooms = booking_service.list_rooms()
    return [RoomOut(number=r.number, room_type=r.room_type) for r in rooms]


@app.get("/rooms/availability", response_model=list[RoomOut])
def check_availability(start: date, end: date):
    rooms = booking_service.available_rooms(start, end)
    return [RoomOut(number=r.number, room_type=r.room_type) for r in rooms]


@app.post("/bookings/{reference}/check-in", response_model=BookingOut)
def check_in(reference: str):
    try:
        booking = booking_service.check_in_booking(reference)
        return BookingOut(**booking.__dict__)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")


@app.post("/bookings/{reference}/check-out", response_model=BookingOut)
def check_out(reference: str):
    try:
        booking = booking_service.check_out_booking(reference)
        return BookingOut(**booking.__dict__)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")


@app.get("/guests/{guest_id}/bookings", response_model=list[BookingOut])
def guest_history(guest_id: str):
    bookings = booking_service.list_guest_bookings(guest_id)
    return [BookingOut(**b.__dict__) for b in bookings]


@app.post("/guests", response_model=GuestOut)
def create_guest(data: GuestIn):
    try:
        guest = booking_service.create_guest(
            data.id, data.first_name, data.last_name, data.date_of_birth
        )
        return GuestOut(**guest.__dict__)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
