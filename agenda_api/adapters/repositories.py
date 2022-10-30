from dataclasses import dataclass
from typing import Type

from sqlalchemy.orm import Session

from agenda_api import domain
from agenda_api.adapters.base import AbstractRepository


@dataclass
class EmployeeRepository(AbstractRepository):
    session: Session
    model: Type[domain.Employee] = domain.Employee


@dataclass
class ClientRepository(AbstractRepository):
    session: Session
    model: Type[domain.Client] = domain.Client


@dataclass
class ServiceRepository(AbstractRepository):
    session: Session
    model: Type[domain.Service] = domain.Service


@dataclass
class AppointmentRepository(AbstractRepository):
    session: Session
    model: Type[domain.Appointment] = domain.Appointment
