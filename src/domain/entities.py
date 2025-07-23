from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum


class RoomType(str, Enum):
    STANDARD = "standard"
    DELUXE = "deluxe"
    SUITE = "suite"

    @property
    def capacity(self) -> int:
        return {self.STANDARD: 2, self.DELUXE: 3, self.SUITE: 4}[self]

    @property
    def price(self) -> int:
        return {self.STANDARD: 100, self.DELUXE: 200, self.SUITE: 300}[self]


@dataclass
class Room:
    number: str
    room_type: RoomType


@dataclass
class Guest:
    id: str
    first_name: str
    last_name: str
    date_of_birth: date

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def is_adult(self) -> bool:
        return self.age >= 18


@dataclass
class Booking:
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
    paid: bool = False
    cancelled: bool = False
    checked_in: bool = False
    checked_out: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)

    def duration(self) -> int:
        return (self.check_out - self.check_in).days

    def overlaps(self, other: "Booking") -> bool:
        return not (self.check_out <= other.check_in or self.check_in >= other.check_out)
