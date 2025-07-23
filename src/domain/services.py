from __future__ import annotations

from datetime import date, timedelta
from typing import List

from .entities import Booking, Guest


class BookingPolicy:
    MAX_NIGHTS = 30
    MIN_NOTICE_HOURS = 24
    MAX_GUESTS = 4

    def validate_new_booking(
        self, guest: Guest, existing_bookings: List[Booking], new_booking: Booking
    ) -> None:
        if not guest.is_adult():
            raise ValueError("Guest must be at least 18 years old")

        if new_booking.number_of_guests > self.MAX_GUESTS:
            raise ValueError("Booking exceeds maximum guest count")

        if new_booking.duration() > self.MAX_NIGHTS:
            raise ValueError("Booking exceeds maximum stay length")

        if (
            new_booking.check_in
            < date.today() + timedelta(hours=self.MIN_NOTICE_HOURS)
        ):
            raise ValueError("Bookings require 24h notice")

        for b in existing_bookings:
            if b.overlaps(new_booking):
                raise ValueError("Room already booked for these dates")
