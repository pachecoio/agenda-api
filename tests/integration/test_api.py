import pytest
from flask import Flask

from agenda_api import domain
from agenda_api.app import create_app
from agenda_api.services.unitofwork import UnitOfWork


def test_create_app():
    app = create_app()
    assert isinstance(app, Flask)


@pytest.fixture
def client(session, session_factory, mocker):
    mocker.patch(
        "agenda_api.services.unitofwork.DEFAULT_SESSION_FACTORY", session_factory
    )
    app = create_app(debug=True)
    return app.test_client()


def test_endpoint_not_found(client):
    res = client.get("/invalid_path")
    assert res.status_code == 404


def test_empty_list_employees(client):
    res = client.get("/api/employees")
    assert res.status_code == 200
    assert res.json == []


@pytest.fixture
def employees(session_factory):
    session = session_factory()
    session.add(domain.Employee("Jon", "Snow"))
    session.add(domain.Employee("Ygritte", "Snow"))
    session.commit()


def test_list_employees(client, session_factory, employees):
    res = client.get("api/employees")
    assert res.status_code == 200
    assert len(res.json) == 2


def test_create_employee(client, session_factory):
    res = client.post("api/employees", json={"first_name": "Jon", "last_name": "Snow"})
    assert res.status_code == 201
    assert res.json["id"]
    assert res.json["first_name"] == "Jon"
    assert res.json["last_name"] == "Snow"


@pytest.fixture
def clients(session_factory):
    session = session_factory()
    session.add(domain.Client("Samwell", "Tarly"))
    session.add(domain.Client("Jorah", "Mormont"))
    session.commit()


def test_list_clients(client, session_factory, clients):
    res = client.get("api/clients")
    assert res.status_code == 200
    assert len(res.json) == 2


def test_create_client(client, session_factory):
    res = client.post(
        "api/clients", json={"first_name": "Samwell", "last_name": "Tarly"}
    )
    assert res.status_code == 201
    assert res.json["id"]
    assert res.json["first_name"] == "Samwell"
    assert res.json["last_name"] == "Tarly"


@pytest.fixture
def services(session_factory):
    session = session_factory()
    session.add(domain.Service("haircut", 5000))
    session.add(domain.Service("Beard", 2500))
    session.commit()


def test_list_services(client, session_factory, services):
    res = client.get("api/services")
    assert res.status_code == 200
    assert len(res.json) == 2


def test_create_service(client, session_factory):
    res = client.post("api/services", json={"name": "haircut", "price": 5000})
    assert res.status_code == 201
    assert res.json["id"]
    assert res.json["name"] == "haircut"
    assert res.json["price"] == 5000
