from dataclasses import asdict

from flask import Blueprint, jsonify, request

from agenda_api.services import commands
from agenda_api.services.handlers import create_employee
from agenda_api.services.unitofwork import get_default_uow

blueprint = Blueprint("employees", __name__, url_prefix="/api")


@blueprint.route("/employees", methods=["GET"])
def list_employees():
    """
    List all employees
    """
    uow = get_default_uow()
    with uow:
        employees = uow.employees.filter()
        items = [asdict(employee) for employee in employees]
    return jsonify(items), 200


@blueprint.route("/employees", methods=["POST"])
def create_employee_endpoint():
    """
    Create a new employee
    """
    uow = get_default_uow()
    with uow:
        cmd = commands.CreateEmployee(**request.json)
        employee = create_employee(uow, cmd)
        uow.commit()
        return jsonify(employee), 201
