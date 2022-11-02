import importlib
import os

from flask import Flask


def create_app(debug=False) -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = debug
    register_resources(app)
    return app


def register_resources(app):
    current_file_path = os.path.dirname(__file__)
    resources_dir = f"{current_file_path}/resources"
    for resource in os.listdir(resources_dir):
        if resource.startswith("__"):
            continue
        module = importlib.import_module(
            f"agenda_api.resources.{resource.replace('.py', '')}"
        )
        app.register_blueprint(module.blueprint)
