from dotenv import load_dotenv
load_dotenv()
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

import os

os.environ['JWT_SECRET'] = 'test_secret'
TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')

from app.db.base import Base
from app.db.session import get_db
from app.main import app

engine = create_engine(TEST_DATABASE_URL)

TestSession = sessionmaker(bind=engine)

def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client