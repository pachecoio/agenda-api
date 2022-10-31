from agenda_api import domain
from agenda_api.adapters.repositories import (
    AppointmentRepository,
    ClientRepository,
    EmployeeRepository,
    ServiceRepository,
)


def test_repo_create_employee(session, session_factory):
    repo = EmployeeRepository(session=session_factory())
    employee = domain.Employee("Jon", "Snow")
    repo.save(employee)
    repo.commit()

    # Reset session to test result
    repo = EmployeeRepository(session=session_factory())
    employees = repo.filter()
    assert employees.count() == 1


def test_repo_create_client(session, session_factory):
    repo = ClientRepository(session=session_factory())
    client = domain.Client("Samwell", "Tarly")
    repo.save(client)
    repo.commit()

    # Reset session to test result
    repo = ClientRepository(session=session_factory())
    clients = repo.filter()
    assert clients.count() == 1


def test_repo_create_service(session, session_factory):
    repo = ServiceRepository(session=session_factory())
    service = domain.Service(
        name="haircut",
        price=5000,
    )
    repo.save(service)
    repo.commit()

    # Reset session to test result
    repo = ServiceRepository(session=session_factory())
    services = repo.filter()
    assert services.count() == 1


def test_repo_create_appointment(session, session_factory):
    repo = AppointmentRepository(session=session_factory())
    appointment = domain.Appointment(
        client_id=1, services={domain.Service("haircut", 5000)}
    )
    repo.save(appointment)
    repo.commit()

    # Reset session to test result
    repo = AppointmentRepository(session=session_factory())
    appointments = repo.filter()
    assert appointments.count() == 1
