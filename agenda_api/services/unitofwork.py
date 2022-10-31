from typing import Callable

from sqlalchemy.orm import Session

from agenda_api.adapters.base import AbstractUnitOfWork
from agenda_api.adapters.repositories import (
    AppointmentRepository,
    ClientRepository,
    EmployeeRepository,
    ServiceRepository,
)


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    @property
    def employees(self):
        return EmployeeRepository(self.session)

    @property
    def clients(self):
        return ClientRepository(self.session)

    @property
    def services(self):
        return ServiceRepository(self.session)

    @property
    def appointments(self):
        return AppointmentRepository(self.session)

    def __enter__(self):
        self.session = self._session_factory()

    def __exit__(self, *args):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
