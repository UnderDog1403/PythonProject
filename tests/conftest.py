import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from core.database import Base
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.dependencies import get_db
from main import app


DATABASETEST_URL = "postgresql://ducanh:halucie2k3@localhost:5432/fastapitest"
engine = create_engine(
    DATABASETEST_URL
)
SessionTesting = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
@pytest.fixture
def db_session():
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def app_test():
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(app_test, db_session):
    def override_get_db():
        yield db_session

    app_test.dependency_overrides[get_db] = override_get_db

    with TestClient(app_test) as client:
        yield client

    app_test.dependency_overrides.clear()



