from dataclasses import dataclass


@dataclass
class EntityNotFound(Exception):
    message: str = "Entity not found"
