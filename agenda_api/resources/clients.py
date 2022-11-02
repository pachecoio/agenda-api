from dataclasses import asdict

from flask import Blueprint, jsonify, request

from agenda_api.services import commands
from agenda_api.services.handlers import create_client
from agenda_api.services.unitofwork import get_default_uow

blueprint = Blueprint("clients", __name__, url_prefix="/api")


@blueprint.route("/clients", methods=["GET"])
def list_clients():
    """
    List all clients
    """
    uow = get_default_uow()
    with uow:
        clients = uow.clients.filter()
        items = [asdict(client) for client in clients]
    return jsonify(items), 200


@blueprint.route("/clients", methods=["POST"])
def create_client_endpoint():
    """
    Create a new client
    """
    uow = get_default_uow()
    with uow:
        cmd = commands.CreateClient(**request.json)
        client = create_client(uow, cmd)
        uow.commit()
        return jsonify(client), 201
