import os
from datetime import datetime

from sqlalchemy import (
    create_engine,
    MetaData,
    Column,
    String,
    Integer,
    orm,
    Table,
    Enum, Boolean, Interval, ForeignKey, DateTime,
)
from sqlalchemy.orm import relationship

from agenda_api import domain

metadata = MetaData()


def get_database_uri() -> str:
    host = os.environ.get("POSTGRES_HOST", "agenda-db")
    port = 5432
    username = os.environ.get("POSTGRES_USER", "root")
    password = os.environ.get("POSTGRES_PASSWORD", "root")
    db_name = os.environ.get("POSTGRES_DB", "agenda")
    return f"postgresql://{username}:{password}@{host}:{port}/{db_name}"


DEFAULT_ENGINE = create_engine(get_database_uri())

DEFAULT_SESSION_FACTORY = orm.sessionmaker(
    bind=DEFAULT_ENGINE
)

employees_table = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
)

clients_table = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
)

services_table = Table(
    "services",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("price", Integer, nullable=False),
    Column("duration", Interval, nullable=False),
)

appointments_table = Table(
    "appointments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("client_id", Integer, ForeignKey("clients.id")),
    Column("status", Enum(domain.AppointmentStatus), nullable=False),
    Column("updated_at", DateTime),
    Column("updated_by", Integer)
)

appointment_services_table = Table(
    "appointment_services",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("appointment_id", Integer, ForeignKey("appointments.id"), nullable=False),
    Column("service_id", Integer, ForeignKey("services.id"), nullable=False),
)


def start_mappers():
    orm.mapper(domain.Employee, employees_table)
    orm.mapper(domain.Client, clients_table)
    services_mapper = orm.mapper(domain.Service, services_table)
    orm.mapper(
        domain.Appointment,
        appointments_table,
        properties={
            "services": relationship(
                services_mapper,
                secondary=appointment_services_table,
                collection_class=set
            )
        }
    )
