from dataclasses import asdict
from typing import TypedDict

from flask import Blueprint, jsonify, request

from agenda_api import domain
from agenda_api.services import commands
from agenda_api.services.handlers import create_employee, create_service
from agenda_api.services.unitofwork import get_default_uow

blueprint = Blueprint("services", __name__, url_prefix="/api")


@blueprint.route("/services", methods=["GET"])
def list_services():
    """
    List all services
    """
    uow = get_default_uow()
    with uow:
        services = uow.services.filter()
        items = [serialize_service(s) for s in services]
    return jsonify(items), 200


@blueprint.route("/services", methods=["POST"])
def create_service_endpoint():
    """
    Create a new service
    """
    uow = get_default_uow()
    with uow:
        cmd = commands.CreateService(**request.json)
        svc = create_service(uow, cmd)
        uow.commit()
        return jsonify(serialize_service(svc)), 201


class ServiceResponse(TypedDict):
    id: str
    name: str
    duration: str


def serialize_service(service: domain.Service) -> ServiceResponse:
    return {
        "id": service.id,
        "name": service.name,
        "price": service.price,
        "duration": str(service.duration),
    }
