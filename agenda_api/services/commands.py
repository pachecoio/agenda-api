from dataclasses import dataclass
from datetime import timedelta
from typing import Optional, Set


@dataclass(frozen=True)
class Command:
    pass


@dataclass(frozen=True)
class CreateEmployee(Command):
    first_name: str
    last_name: str


@dataclass(frozen=True)
class CreateClient(Command):
    first_name: str
    last_name: str


@dataclass(frozen=True)
class CreateService(Command):
    name: str
    price: int
    duration: Optional[timedelta] = None


@dataclass(frozen=True)
class CreateAppointment(Command):
    client_id: int
    service_ids: Set[int]
