import abc
from typing import Type, Dict

from sqlalchemy.orm import Session, Query


class AbstractRepository(abc.ABC):
    session: Session
    model: Type[any]

    def save(self, entity):
        """Base method to save an entity"""
        self.session.add(entity)

    def filter(self, **kwargs) -> Query:
        """Base method to filter entities"""
        return self.session.query(self.model).filter_by(**kwargs)

    def delete(self, model):
        """Base method to delete an entity"""
        self.session.delete(model)

    def commit(self):
        """Base method to commit db changes"""
        self.session.commit()

    def rollback(self):
        """Base method to rollback db changes"""
        self.session.rollback()


class AbstractUnitOfWork(abc.ABC):
    session: Session
    employees: AbstractRepository
    clients: AbstractRepository
    services: AbstractRepository
    appointments: AbstractRepository

    @abc.abstractmethod
    def __enter__(self):
        """Initialize the unit of work"""

    @abc.abstractmethod
    def __exit__(self, *args):
        """Exit unit of work"""

    @abc.abstractmethod
    def commit(self):
        """Commit changes to the database"""
        self.session.commit()

    @abc.abstractmethod
    def rollback(self):
        """Rollback changes to the database"""
        self.session.rollback()
