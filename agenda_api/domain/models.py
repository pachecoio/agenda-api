import enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Set

from agenda_api.domain import errors


@dataclass
class User:
    first_name: str
    last_name: str
    id: int = field(init=False)

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass
class Employee(User):
    pass


@dataclass
class Client(User):
    pass


@dataclass(unsafe_hash=True, init=False)
class Service:
    name: str
    price: int
    id: int = field(init=False)
    duration: timedelta = field(default_factory=lambda: timedelta(hours=1))

    def __init__(self, name: str, price: int, duration: timedelta = None):
        if price < 1:
            raise errors.ServiceError("Cannot create service with negative price")
        if not duration:
            duration = timedelta(hours=1)
        if duration <= timedelta(0):
            raise errors.ServiceError("Cannot create service with negative duration")
        self.name = name
        self.price = price
        self.duration = duration


class AppointmentStatus(enum.Enum):
    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELED = "canceled"


@dataclass(unsafe_hash=True)
class Appointment:
    client_id: int
    services: Set[Service]
    status: AppointmentStatus = AppointmentStatus.PENDING
    updated_at: Optional[datetime] = None
    updated_by: Optional[Employee] = None
    id: int = field(init=False)

    @property
    def total_price(self) -> int:
        return sum(service.price for service in self.services)

    @property
    def total_duration(self) -> timedelta:
        duration = timedelta(hours=0)
        for service in self.services:
            duration += service.duration
        return duration

    def start(self):
        if self.status != AppointmentStatus.PENDING:
            raise errors.AppointmentError(
                f"Cannot start an appointment with status {self.status.value}"
            )
        self.status = AppointmentStatus.STARTED

    def complete(self, employee: Employee):
        if self.status == AppointmentStatus.CANCELED:
            raise errors.AppointmentError(
                f"Cannot complete an appointment with status {self.status.value}"
            )
        self.status = AppointmentStatus.COMPLETED
        self.updated_by = employee

    def cancel(self, employee: Employee):
        if self.status == AppointmentStatus.COMPLETED:
            raise errors.AppointmentError(
                f"Cannot cancel an appointment with status {self.status.value}"
            )
        self.status = AppointmentStatus.CANCELED
        self.updated_by = employee
