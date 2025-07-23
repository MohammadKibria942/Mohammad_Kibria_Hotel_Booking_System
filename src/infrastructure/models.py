from __future__ import annotations

from datetime import date, datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date, Boolean, DateTime


class Base(DeclarativeBase):
    pass


class GuestModel(Base):
    __tablename__ = "guests"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[date] = mapped_column(Date)


class RoomModel(Base):
    __tablename__ = "rooms"

    number: Mapped[str] = mapped_column(String, primary_key=True)
    room_type: Mapped[str] = mapped_column(String)


class BookingModel(Base):
    __tablename__ = "bookings"

    reference: Mapped[str] = mapped_column(String, primary_key=True)
    guest_id: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[date] = mapped_column(Date)
    room_type: Mapped[str] = mapped_column(String)
    room_number: Mapped[str] = mapped_column(String)
    number_of_guests: Mapped[int] = mapped_column()
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    paid: Mapped[bool] = mapped_column(Boolean)
    cancelled: Mapped[bool] = mapped_column(Boolean)
    checked_in: Mapped[bool] = mapped_column(Boolean, default=False)
    checked_out: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime)
