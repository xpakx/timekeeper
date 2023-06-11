from fastapi.testclient import TestClient
import pytest
from timekeeper.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timekeeper.db.base import Base
from timekeeper.db.manager import get_db
from timekeeper.db.models import User, Timer, TimerInstance, TimerState
from bcrypt import hashpw, gensalt
from timekeeper.services.user_service import create_token
from datetime import datetime
from sqlalchemy.sql import func

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
TestingSessionLocal = sessionmaker(autocommit=False,
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


def create_timer(name: str, user_id: int) -> int:
    return create_timer_(name, user_id, False)


def create_timer_(name: str, user_id: int, deleted: bool) -> int:
    db = TestingSessionLocal()
    new_timer = Timer(
            name=name,
            description="",
            duration_s=100,
            deleted=deleted,
            owner_id=user_id
            )
    db.add(new_timer)
    db.commit()
    db.refresh(new_timer)
    db.close()
    return new_timer.id


def create_timer_instance(user_id: int, timer_id: int) -> int:
    db = TestingSessionLocal()
    new_timer = TimerInstance(
            state=TimerState.running,
            timer_id=timer_id,
            owner_id=user_id,
            start_time=func.now()
            )
    db.add(new_timer)
    db.commit()
    db.refresh(new_timer)
    db.close()
    return new_timer.id


def get_token() -> str:
    return get_token_for(1)


def get_token_for(user_id: int) -> str:
    return create_token({"id": f"{user_id}", "sub": "User"})


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_adding_timer_without_authentication(test_db):
    response = client.post("/timers/",
                           json={
                               "name": "New timer",
                               "description": "desc",
                               "duration_s": "1500"
                               }
                           )
    assert response.status_code == 401


def test_adding_timer_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/timers/",
                           json={
                               "name": "New timer",
                               "description": "desc",
                               "duration_s": "1500"
                               },
                           headers=headers
                           )
    assert response.status_code == 401


def test_adding_timer(test_db):
    create_user()
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.post("/timers/",
                           json={
                               "name": "New timer",
                               "description": "desc",
                               "duration_s": "1500"
                               },
                           headers=headers
                           )
    assert response.status_code == 200


def test_adding_timer_with_negative_duration(test_db):
    create_user()
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.post("/timers/",
                           json={
                               "name": "New timer",
                               "description": "desc",
                               "duration_s": "-1"
                               },
                           headers=headers
                           )
    assert response.status_code == 400


def test_adding_timer_with_zero_duration(test_db):
    create_user()
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.post("/timers/",
                           json={
                               "name": "New timer",
                               "description": "desc",
                               "duration_s": "0"
                               },
                           headers=headers
                           )
    assert response.status_code == 400


def test_adding_timer_with_empty_name(test_db):
    create_user()
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.post("/timers/",
                           json={
                               "name": "",
                               "description": "desc",
                               "duration_s": "1500"
                               },
                           headers=headers
                           )
    assert response.status_code == 400


@pytest.mark.skip(reason="todo")
def test_adding_timer_with_whitespace_only_name(test_db):
    create_user()
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.post("/timers/",
                           json={
                               "name": "   ",
                               "description": "desc",
                               "duration_s": "1500"
                               },
                           headers=headers
                           )
    assert response.status_code == 400


def test_getting_timers_without_authentication(test_db):
    response = client.get("/timers/")
    assert response.status_code == 401


def test_getting_timers_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/timers/",
                          headers=headers
                          )
    assert response.status_code == 401


def test_getting_users_timers(test_db):
    id = create_user_and_return_id()
    create_timer("Test", id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]['name'] == "Test"


def test_not_getting_other_users_timers(test_db):
    id = create_user_and_return_id()
    other = create_user_with_username("User2")
    create_timer("Test", id)
    create_timer("Other", other)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]['name'] == "Test"


def test_getting_first_page_of_timers(test_db):
    id = create_user_and_return_id()
    create_timer("Test1", id)
    create_timer("Test2", id)
    create_timer("Test3", id)
    create_timer("Test4", id)
    create_timer("Test5", id)
    create_timer("Test6", id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/?page=0&size=5",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 5


def test_getting_second_page_of_timers(test_db):
    id = create_user_and_return_id()
    create_timer("Test1", id)
    create_timer("Test2", id)
    create_timer("Test3", id)
    create_timer("Test4", id)
    create_timer("Test5", id)
    create_timer("Test6", id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/?page=1&size=5",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1


def test_getting_to_large_page_of_timers(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/?page=0&size=125",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_negative_page_of_timers(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/?page=-2&size=5",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_negative_amount_of_timers(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/?page=0&size=-5",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_timers_with_default_values(test_db):
    id = create_user_and_return_id()
    for i in range(0, 30):
        create_timer(f"Test{i}", id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 20


def test_not_getting_deleted_timers(test_db):
    id = create_user_and_return_id()
    create_timer("Test", id)
    create_timer_("Deleted", id, True)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]['name'] == "Test"


# editing
def test_editing_timer_without_authentication(test_db):
    response = client.put("/timers/1",
                          json={
                               "name": "New timer",
                               "description": "desc",
                               "duration_s": "1500"
                               }
                          )
    assert response.status_code == 401


def test_editing_timer_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.put("/timers/1",
                          json={
                               "name": "New timer",
                               "description": "desc",
                               "duration_s": "1500"
                               },
                          headers=headers
                          )
    assert response.status_code == 401


def test_editing_timer(test_db):
    user_id = create_user_and_return_id()
    id = create_timer("Test", user_id)
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.put(f"/timers/{id}",
                          json={
                               "name": "Updated timer",
                               "description": "desc",
                               "duration_s": "1500"
                               },
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert result['name'] == "Updated timer"


def test_editing_timer_with_negative_duration(test_db):
    user_id = create_user_and_return_id()
    id = create_timer("Test", user_id)
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.put(f"/timers/{id}",
                          json={
                               "name": "Updated timer",
                               "description": "desc",
                               "duration_s": "-1"
                               },
                          headers=headers
                          )
    assert response.status_code == 400


def test_editing_timer_with_zero_duration(test_db):
    user_id = create_user_and_return_id()
    id = create_timer("Test", user_id)
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.put(f"/timers/{id}",
                          json={
                               "name": "Updated timer",
                               "description": "desc",
                               "duration_s": "0"
                               },
                          headers=headers
                          )
    assert response.status_code == 400


def test_editing_timer_with_empty_name(test_db):
    user_id = create_user_and_return_id()
    id = create_timer("Test", user_id)
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.put(f"/timers/{id}",
                          json={
                               "name": "",
                               "description": "desc",
                               "duration_s": "1500"
                               },
                          headers=headers
                          )
    assert response.status_code == 400


@pytest.mark.skip(reason="todo")
def test_editing_timer_with_whitespace_only_name(test_db):
    user_id = create_user_and_return_id()
    id = create_timer("Test", user_id)
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.put(f"/timers/{id}",
                          json={
                               "name": "  ",
                               "description": "desc",
                               "duration_s": "1500"
                               },
                          headers=headers
                          )
    assert response.status_code == 400


def test_editing_other_users_timer(test_db):
    user_id = create_user_and_return_id()
    other_id = create_user_with_username("Other")
    id = create_timer("Test", other_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.put(f"/timers/{id}",
                          json={
                               "name": "Updated timer",
                               "description": "desc",
                               "duration_s": "1500"
                               },
                          headers=headers
                          )
    assert response.status_code == 401


# deleting
def test_deleting_timer_without_authentication(test_db):
    response = client.delete("/timers/1")
    assert response.status_code == 401


def test_deleting_timer_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.delete("/timers/1", headers=headers)
    assert response.status_code == 401


def test_deleting_timer(test_db):
    user_id = create_user_and_return_id()
    id = create_timer("Test", user_id)
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.delete(f"/timers/{id}", headers=headers)
    assert response.status_code == 200


def test_deleting_other_users_timer(test_db):
    user_id = create_user_and_return_id()
    other_id = create_user_with_username("Other")
    id = create_timer("Test", other_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.delete(f"/timers/{id}", headers=headers)
    assert response.status_code == 401


# starting
def test_starting_timer_without_authentication(test_db):
    response = client.post("/timers/1/instances")
    assert response.status_code == 401


def test_starting_timer_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/timers/1/instances", headers=headers)
    assert response.status_code == 401


def test_starting_other_users_timer(test_db):
    user_id = create_user_and_return_id()
    other_id = create_user_with_username("Other")
    id = create_timer("Test", other_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/timers/{id}/instances", headers=headers)
    assert response.status_code == 401


def test_starting_non_existent_timer(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/timers/1/instances", headers=headers)
    assert response.status_code == 401


def test_starting_timer(test_db):
    user_id = create_user_and_return_id()
    id = create_timer("Test", user_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/timers/{id}/instances", headers=headers)
    assert response.status_code == 200


def test_adding_started_timer_instance_to_db_with_owner(test_db):
    user_id = create_user_and_return_id()
    id = create_timer("Test", user_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    client.post(f"/timers/{id}/instances", headers=headers)
    db = TestingSessionLocal()
    timer: TimerInstance = db.query(TimerInstance).first()
    db.close()
    assert timer.owner_id == user_id


# changing state
def test_changing_timer_state_without_authentication(test_db):
    response = client.post("/timers/instances/1/state")
    assert response.status_code == 401


def test_changing_timer_state_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/timers/instances/1/state", headers=headers)
    assert response.status_code == 401


def test_changing_other_users_timer_state(test_db):
    user_id = create_user_and_return_id()
    other_id = create_user_with_username("Other")
    timer_id = create_timer("Test", other_id)
    id = create_timer_instance(other_id, timer_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/timers/instances/{id}/state",
                           headers=headers,
                           json={"state": "finished"})
    assert response.status_code == 401


def test_changing_non_existent_timer_state(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/timers/instances/1/state",
                           headers=headers,
                           json={"state": "finished"})
    assert response.status_code == 401


def test_changing_timer_state(test_db):
    user_id = create_user_and_return_id()
    timer_id = create_timer("Test", user_id)
    id = create_timer_instance(user_id, timer_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/timers/instances/{id}/state",
                           headers=headers,
                           json={"state": "finished"})
    assert response.status_code == 200


# getting active timers
def test_getting_active_timers_without_authentication(test_db):
    response = client.get("/timers/active")
    assert response.status_code == 401


def test_getting_active_timers_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/timers/active",
                          headers=headers
                          )
    assert response.status_code == 401


def test_getting_users_active_timers(test_db):
    user_id = create_user_and_return_id()
    timer_id = create_timer("Test", user_id)
    create_timer_instance(user_id, timer_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/timers/active",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1


def test_not_getting_other_users_active_timers(test_db):
    id = create_user_and_return_id()
    other = create_user_with_username("User2")
    timer_id = create_timer("Test", other)
    user_timer = create_timer("Test", id)
    create_timer_instance(other, timer_id)
    create_timer_instance(id, user_timer)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/active",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1


def test_getting_first_page_of_active_timers(test_db):
    id = create_user_and_return_id()
    timer = create_timer("Test", id)
    for i in range(0, 6):
        create_timer_instance(id, timer)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/active/?page=0&size=5",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 5


def test_getting_second_page_of_active_timers(test_db):
    id = create_user_and_return_id()
    timer = create_timer("Test", id)
    for i in range(0, 6):
        create_timer_instance(id, timer)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/active/?page=1&size=5",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1


def test_getting_to_large_page_of_active_timers(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/active/?page=0&size=125",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_negative_page_of_active_timers(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/active/?page=-2&size=5",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_negative_amount_of_active_timers(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/active/?page=0&size=-5",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_active_timers_with_default_values(test_db):
    id = create_user_and_return_id()
    timer = create_timer("Test", id)
    for i in range(0, 30):
        create_timer_instance(id, timer)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/timers/active",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 20