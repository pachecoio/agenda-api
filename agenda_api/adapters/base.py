import abc
from typing import Type

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
