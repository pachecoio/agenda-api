from typing import Set

import pytest

from agenda_api import domain
from agenda_api.adapters.repositories import EmployeeRepository, ClientRepository, ServiceRepository, \
    AppointmentRepository
from agenda_api.services import commands
from agenda_api.services.errors import EntityNotFound
from agenda_api.services.handlers import create_employee, create_client, create_service, create_appointment
from agenda_api.services.unitofwork import UnitOfWork


def test_create_employee(session, session_factory):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CreateEmployee("Jon", "Snow")
        create_employee(uow, cmd)
        uow.commit()

    repo = EmployeeRepository(session=session_factory())
    employees = repo.filter()
    assert employees.count() == 1


def test_create_client(session, session_factory):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CreateClient("Jon", "Snow")
        create_client(uow, cmd)
        uow.commit()

    repo = ClientRepository(session=session_factory())
    clients = repo.filter()
    assert clients.count() == 1


def test_create_service(session, session_factory):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CreateService(
            name="haircut",
            price=5000
        )
        create_service(uow, cmd)
        uow.commit()

    repo = ServiceRepository(session=session_factory())
    services = repo.filter()
    assert services.count() == 1


@pytest.fixture
def services(session_factory) -> Set[domain.Service]:
    service = domain.Service("haircut", 5000)
    repo = ServiceRepository(session=session_factory())
    repo.save(service)
    repo.commit()
    return {service}


@pytest.fixture
def client(session_factory) -> domain.Client:
    client = domain.Client(
        "Jon",
        "Snow",
    )
    repo = ClientRepository(session=session_factory())
    repo.save(client)
    repo.commit()
    return client


def test_create_appointment(session, session_factory, client, services):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CreateAppointment(
            client_id=client.id,
            service_ids={service.id for service in services}
        )
        create_appointment(uow, cmd)
        uow.commit()

    repo = AppointmentRepository(session=session_factory())
    appointments = repo.filter()
    assert appointments.count() == 1


def test_cannot_create_appointment_service_not_found(session, session_factory):
    uow = UnitOfWork(session_factory=session_factory)
    with pytest.raises(EntityNotFound), uow:
        cmd = commands.CreateAppointment(
            client_id=1,
            service_ids={1}
        )
        create_appointment(uow, cmd)


def test_cannot_create_appointment_client_not_found(session, session_factory, services):
    uow = UnitOfWork(session_factory=session_factory)
    with pytest.raises(EntityNotFound) as e, uow:
        cmd = commands.CreateAppointment(
            client_id=1,
            service_ids={service.id for service in services}
        )
        create_appointment(uow, cmd)

    assert e.value.message == f"Client with id {1} not found"
