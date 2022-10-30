from dataclasses import dataclass


@dataclass
class ServiceError(Exception):
    message: str = "Service error"


@dataclass
class AppointmentError(Exception):
    message: str = "Appointment error"
