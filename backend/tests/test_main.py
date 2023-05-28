from fastapi.testclient import TestClient
import pytest
from timekeeper.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timekeeper.db.base import Base
from timekeeper.db.manager import get_db

url = URL.create("postgresql", "root", "password", "localhost", 5432, "time_db_test")

engine = create_engine(
    url, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_user():
    response = client.post("/users/register",
                           json={
                               "username": "User1",
                               "password": "password",
                               "repeated_password": "password"
                               }
                           )
    assert response.status_code == 200
    assert response.json() == {"msg200": "Hello World"}
