from dataclasses import dataclass
from typing import Type, Set

from sqlalchemy.orm import Session, Query

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

    def filter(self, ids: Set[int] = None, **kwargs) -> Query:
        query = self.session.query(self.model)
        if ids:
            query = query.filter(
                self.model.id.in_(ids)
            )
        query = query.filter_by(**kwargs)
        return query


@dataclass
class AppointmentRepository(AbstractRepository):
    session: Session
    model: Type[domain.Appointment] = domain.Appointment
