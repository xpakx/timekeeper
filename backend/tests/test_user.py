
from fastapi.testclient import TestClient
import pytest
from timekeeper.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timekeeper.db.base import Base
from timekeeper.db.manager import get_db
from timekeeper.db.models import User
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


def create_user_and_return_id() -> int:
    return create_user_with_username("User")


def get_token() -> str:
    return get_token_for(1)


def get_token_for(user_id: int) -> str:
    return create_token({"id": f"{user_id}", "sub": "User"})


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_user(test_db):
    response = client.post("/users/register",
                           json={
                               "username": "User1",
                               "password": "password",
                               "repeated_password": "password"
                               }
                           )
    assert response.status_code == 200
    result = response.json()
    assert result['username'] == "User1"
    assert result['token'] is not None


def test_repeated_password_shuld_be_the_same(test_db):
    response = client.post("/users/register",
                           json={
                               "username": "User1",
                               "password": "password",
                               "repeated_password": "password1"
                               }
                           )
    assert response.status_code == 400


def test_not_register_user_with_already_taken_username(test_db):
    create_user()
    response = client.post("/users/register",
                           json={
                               "username": "User",
                               "password": "password",
                               "repeated_password": "password"
                               }
                           )
    assert response.status_code == 400


def test_add_user_to_db(test_db):
    client.post("/users/register",
                json={
                    "username": "User1",
                    "password": "password",
                    "repeated_password": "password"
                    }
                )
    db = TestingSessionLocal()
    users = db.query(User).count()
    db.close()
    assert users == 1


def test_authentication_with_wrong_password(test_db):
    create_user()
    response = client.post("/users/login",
                           json={
                               "username": "User",
                               "password": "wrong_password",
                               }
                           )
    assert response.status_code == 403


def test_authentication_for_nonexistent_user(test_db):
    response = client.post("/users/login",
                           json={
                               "username": "User",
                               "password": "password",
                               }
                           )
    assert response.status_code == 404


def test_authentication(test_db):
    create_user()
    response = client.post("/users/login",
                           json={
                               "username": "User",
                               "password": "password",
                               }
                           )
    assert response.status_code == 200
    result = response.json()
    assert result['username'] == "User"
    assert result['token'] is not None
