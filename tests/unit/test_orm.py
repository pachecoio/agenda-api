from sqlalchemy.orm import session

from agenda_api import domain


def test_can_create_employee(session):
    session.execute(
        "INSERT INTO employees (first_name, last_name) VALUES ('Jon', 'Snow')"
    )
    employees = session.execute(
        "SELECT first_name, last_name FROM employees"
    ).fetchall()
    assert len(employees) == 1


def test_can_create_client(session):
    session.execute(
        "INSERT INTO clients (first_name, last_name) VALUES ('Jon', 'Snow')"
    )
    clients = session.execute(
        "SELECT first_name, last_name FROM clients"
    ).fetchall()
    assert len(clients) == 1


def test_can_create_service(session):
    haircut = domain.Service(
        "haircut",
        5000,
    )
    session.add(haircut)
    session.commit()

    services = session.query(domain.Service)
    assert services.count() == 1

    service = services.first()
    assert service == haircut


def test_can_create_appointment(session):
    haircut = domain.Service("haircut", 5000)
    appointment = domain.Appointment(
        client_id=1,
        services={haircut}
    )
    session.add(appointment)
    session.commit()

    appointments = session.query(domain.Appointment)
    assert appointments.count() == 1
    appointment = appointments.first()
    assert next(iter(appointment.services)) == haircut
    assert appointment.client_id == 1
    assert not appointment.updated_at
    assert not appointment.updated_by

