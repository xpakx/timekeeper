from fastapi.testclient import TestClient
import pytest
from timekeeper.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timekeeper.db.base import Base
from timekeeper.db.manager import get_db
from timekeeper.db.models import User, Points
from bcrypt import hashpw, gensalt
from timekeeper.services.user_service import create_token

url = URL.create(
        "postgresql",
        "root",
        "password",
        "localhost",
        5432,
        "time_db_test")

engine = create_engine(
    url
)
TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)


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


def create_user():
    db = TestingSessionLocal()
    password = hashpw("password".encode('utf-8'), gensalt()).decode()
    new_user = User(
            username="User",
            password=password
            )
    db.add(new_user)
    db.commit()
    db.close()


def create_user_with_username(username: str) -> int:
    db = TestingSessionLocal()
    password = hashpw("password".encode('utf-8'), gensalt()).decode()
    new_user = User(
            username=username,
            password=password
            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user.id


def add_points_for_user(user_id: int, points: int):
    db = TestingSessionLocal()
    points_db = Points(
            user_id=user_id,
            points=points
            )
    db.add(points_db)
    db.commit()
    db.close()


def create_user_and_return_id() -> int:
    return create_user_with_username("User")


def get_token() -> str:
    return get_token_for(1)


def get_token_for(user_id: int) -> str:
    return create_token({"id": f"{user_id}", "sub": "User"})


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_getting_points_without_authentication(test_db):
    response = client.get("/points")
    assert response.status_code == 401


def test_getting_points_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/points", headers=headers)
    assert response.status_code == 401


def test_getting_points_if_there_is_no_points_entry(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/points", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result['points'] == 0


def test_getting_points(test_db):
    user_id = create_user_and_return_id()
    add_points_for_user(user_id, 10)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/points", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result['points'] == 10
