from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from .entities import Booking, Guest, Room


class GuestRepository(ABC):
    @abstractmethod
    def add(self, guest: Guest) -> None:
        pass

    @abstractmethod
    def get(self, guest_id: str) -> Optional[Guest]:
        pass


class RoomRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[Room]:
        pass

    @abstractmethod
    def get(self, number: str) -> Optional[Room]:
        pass


class BookingRepository(ABC):
    @abstractmethod
    def add(self, booking: Booking) -> None:
        pass

    @abstractmethod
    def get(self, reference: str) -> Optional[Booking]:
        pass

    @abstractmethod
    def list_for_room(self, room_number: str) -> List[Booking]:
        pass

    @abstractmethod
    def list_for_guest(self, guest_id: str) -> List[Booking]:
        pass

    @abstractmethod
    def remove(self, reference: str) -> None:
        pass

    @abstractmethod
    def list_between(self, start: date, end: date) -> List[Booking]:
        pass

    @abstractmethod
    def update(self, booking: Booking) -> None:
        pass
