from typing import Set

import pytest

from agenda_api import domain
from agenda_api.adapters.repositories import (
    AppointmentRepository,
    ClientRepository,
    EmployeeRepository,
    ServiceRepository,
)
from agenda_api.services import commands
from agenda_api.services.errors import EntityNotFound
from agenda_api.services.handlers import (
    cancel_appointment,
    complete_appointment,
    create_appointment,
    create_client,
    create_employee,
    create_service,
)
from agenda_api.services.unitofwork import UnitOfWork


@pytest.fixture
def appointment(session_factory, client, services):
    apt = domain.Appointment(client_id=client.id, services=services)
    repo = AppointmentRepository(session=session_factory())
    repo.save(apt)
    repo.commit()
    return apt


@pytest.fixture
def employee(session_factory):
    employee = domain.Employee("Jon", "Snow")
    repo = EmployeeRepository(session=session_factory())
    repo.save(employee)
    repo.commit()
    return employee


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


def test_create_employee(session, session_factory):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CreateEmployee("Jon", "Snow")
        employee = create_employee(uow, cmd)
        uow.commit()
        assert employee.id

    repo = EmployeeRepository(session=session_factory())
    employees = repo.filter()
    assert employees.count() == 1


def test_create_client(session, session_factory):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CreateClient("Jon", "Snow")
        client = create_client(uow, cmd)
        uow.commit()
        assert client.id

    repo = ClientRepository(session=session_factory())
    clients = repo.filter()
    assert clients.count() == 1


def test_create_service(session, session_factory):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CreateService(name="haircut", price=5000)
        create_service(uow, cmd)
        uow.commit()

    repo = ServiceRepository(session=session_factory())
    services = repo.filter()
    assert services.count() == 1


def test_create_appointment(session, session_factory, client, services):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CreateAppointment(
            client_id=client.id, service_ids={service.id for service in services}
        )
        create_appointment(uow, cmd)
        uow.commit()

    repo = AppointmentRepository(session=session_factory())
    appointments = repo.filter()
    assert appointments.count() == 1


def test_cannot_create_appointment_service_not_found(session, session_factory):
    uow = UnitOfWork(session_factory=session_factory)
    with pytest.raises(EntityNotFound), uow:
        cmd = commands.CreateAppointment(client_id=1, service_ids={1})
        create_appointment(uow, cmd)


def test_cannot_create_appointment_client_not_found(session, session_factory, services):
    uow = UnitOfWork(session_factory=session_factory)
    with pytest.raises(EntityNotFound) as e, uow:
        cmd = commands.CreateAppointment(
            client_id=1, service_ids={service.id for service in services}
        )
        create_appointment(uow, cmd)

    assert e.value.message == f"Client with id {1} not found"


def test_cannot_complete_appointment_not_found(session, session_factory, employee):
    uow = UnitOfWork(session_factory=session_factory)
    with pytest.raises(EntityNotFound) as e, uow:
        cmd = commands.CompleteAppointment(appointment_id=1, employee_id=employee.id)
        complete_appointment(uow, cmd)
        uow.commit()


def test_complete_appointment(session, session_factory, appointment, employee):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CompleteAppointment(
            appointment_id=appointment.id,
            employee_id=employee.id,
        )
        complete_appointment(uow, cmd)
        uow.commit()

    repo = AppointmentRepository(session=session_factory())
    appointments = repo.filter()
    assert appointments.count() == 1
    appointment_found = appointments.first()
    assert appointment_found.status == domain.AppointmentStatus.COMPLETED


def test_cannot_cancel_appointment_not_found(session, session_factory):
    uow = UnitOfWork(session_factory=session_factory)
    with pytest.raises(EntityNotFound) as e, uow:
        cmd = commands.CancelAppointment(
            appointment_id=1,
            employee_id=1,
        )
        cancel_appointment(uow, cmd)
        uow.commit()


def test_cancel_appointment(session, session_factory, appointment, employee):
    uow = UnitOfWork(session_factory=session_factory)
    with uow:
        cmd = commands.CancelAppointment(
            appointment_id=appointment.id,
            employee_id=employee.id,
        )
        cancel_appointment(uow, cmd)
        uow.commit()

    repo = AppointmentRepository(session=session_factory())
    appointments = repo.filter()
    assert appointments.count() == 1
    appointment_found = appointments.first()
    assert appointment_found.status == domain.AppointmentStatus.CANCELED
