from datetime import timedelta

import pytest

from agenda_api import domain
from agenda_api.domain import errors


def test_employee_instance():
    employee = domain.Employee("Jon", "Snow")
    assert employee.name == "Jon Snow"


def test_client_instance():
    client = domain.Client("Samwell", "Tarly")
    assert client.name == "Samwell Tarly"


def test_service():
    haircut = domain.Service("haircut", 5000)
    assert haircut.name == "haircut"
    assert haircut.price == 5000
    assert haircut.duration == timedelta(hours=1)


def test_cannot_create_service_invalid_price():
    with pytest.raises(errors.ServiceError) as e:
        domain.Service("haircut", -1)
    assert e.value.message == "Cannot create service with negative price"


def test_cannot_create_service_invalid_duration():
    with pytest.raises(errors.ServiceError) as e:
        domain.Service("haircut", 5000, timedelta(hours=-1))
    assert e.value.message == "Cannot create service with negative duration"


def test_appointment():
    haircut = domain.Service("haircut", 5000)
    bear_trim = domain.Service("Bear trim", 2500, duration=timedelta(minutes=30))
    services = set()
    services.add(haircut)
    services.add(bear_trim)
    appointment = domain.Appointment(
        client_id=1,
        services=services
    )
    assert len(appointment.services) == 2
    assert appointment.status == domain.AppointmentStatus.PENDING
    assert appointment.total_price == 7500
    assert appointment.total_duration == timedelta(hours=1, minutes=30)


@pytest.fixture
def sample_appointment() -> domain.Appointment:
    haircut = domain.Service("haircut", 5000)
    return domain.Appointment(
        client_id=1,
        services={haircut}
    )


@pytest.fixture
def employee():
    return domain.Employee("Jon", "Snow")


def test_start_appointment(sample_appointment, employee):
    assert sample_appointment.status == domain.AppointmentStatus.PENDING
    sample_appointment.start()
    assert sample_appointment.status == domain.AppointmentStatus.STARTED


def test_complete_appointment(sample_appointment, employee):
    assert sample_appointment.status == domain.AppointmentStatus.PENDING
    sample_appointment.complete(employee)
    assert sample_appointment.status == domain.AppointmentStatus.COMPLETED
    assert sample_appointment.updated_by == employee


def test_cancel_appointment(sample_appointment, employee):
    assert sample_appointment.status == domain.AppointmentStatus.PENDING
    sample_appointment.cancel(employee)
    assert sample_appointment.status == domain.AppointmentStatus.CANCELED
    assert sample_appointment.updated_by == employee


def test_cannot_start_appointment_completed(sample_appointment):
    sample_appointment.status = domain.AppointmentStatus.COMPLETED
    with pytest.raises(errors.AppointmentError) as e:
        sample_appointment.start()
    assert e.value.message == f"Cannot start an appointment with status {sample_appointment.status.value}"


def test_cannot_start_appointment_canceled(sample_appointment, employee):
    sample_appointment.complete(employee)
    with pytest.raises(errors.AppointmentError) as e:
        sample_appointment.start()
    assert e.value.message == f"Cannot start an appointment with status {sample_appointment.status.value}"


def test_cannot_complete_appointment_canceled(sample_appointment, employee):
    sample_appointment.cancel(employee)
    with pytest.raises(errors.AppointmentError) as e:
        sample_appointment.complete(employee)
    assert e.value.message == f"Cannot complete an appointment with status {sample_appointment.status.value}"


def test_cannot_cancel_appointment_completed(sample_appointment, employee):
    sample_appointment.complete(employee)
    with pytest.raises(errors.AppointmentError) as e:
        sample_appointment.cancel(employee)
    assert e.value.message == f"Cannot cancel an appointment with status {sample_appointment.status.value}"
