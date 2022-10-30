from dataclasses import asdict

from agenda_api import domain
from agenda_api.adapters.base import AbstractUnitOfWork
from agenda_api.services import commands
from agenda_api.services.errors import EntityNotFound


def create_employee(uow: AbstractUnitOfWork, cmd: commands.Command):
    employee = domain.Employee(**asdict(cmd))
    uow.employees.save(employee)


def create_client(uow: AbstractUnitOfWork, cmd: commands.Command):
    client = domain.Client(**asdict(cmd))
    uow.clients.save(client)


def create_service(uow: AbstractUnitOfWork, cmd: commands.Command):
    service = domain.Service(**asdict(cmd))
    uow.services.save(service)


def create_appointment(uow: AbstractUnitOfWork, cmd: commands.CreateAppointment):
    client = uow.clients.filter(id=cmd.client_id).first()
    if not client:
        raise EntityNotFound(f'Client with id {cmd.client_id} not found')
    services = uow.services.filter(ids=cmd.service_ids).all()
    if len(services) < len(cmd.service_ids):
        raise EntityNotFound("Services not found")
    appointment = domain.Appointment(
        client_id=cmd.client_id,
        services=set(services)
    )
    uow.appointments.save(appointment)

