import pytest
from sqlalchemy import create_engine, orm

from agenda_api.adapters.orm import metadata, start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    return orm.sessionmaker(bind=in_memory_db, expire_on_commit=False)


@pytest.fixture
def session(session_factory):
    start_mappers()
    yield session_factory()
    orm.clear_mappers()
