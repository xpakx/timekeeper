from fastapi.testclient import TestClient
import pytest
from timekeeper.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timekeeper.db.base import Base
from timekeeper.db.manager import get_db
from timekeeper.db.models import (
        User,
        Hero,
        UserHero,
        ItemRarity,
        Team)
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


def create_team(user_id: int) -> int:
    db = TestingSessionLocal()
    team = Team(
            user_id=user_id
            )
    db.add(team)
    db.commit()
    db.refresh(team)
    db.close()
    return team.id


def add_to_team(team_id: int, hero_id: int, num: int):
    db = TestingSessionLocal()
    team = db.get(Team, team_id)
    if num == 1:
        team.hero_1_id = hero_id
    if num == 2:
        team.hero_2_id = hero_id
    if num == 3:
        team.hero_3_id = hero_id
    if num == 4:
        team.hero_4_id = hero_id
    if num == 5:
        team.hero_5_id = hero_id
    if num == 6:
        team.hero_6_id = hero_id
    db.commit()
    db.close()


def create_hero(id: int, name: str) -> int:
    db = TestingSessionLocal()
    item = Hero(
            num=id,
            name=name,
            description="",
            rarity=ItemRarity.uncommon
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_user_hero(
        hero_id: int,
        user_id: int,
        incubated: bool = False,
        in_team: bool = False):
    db = TestingSessionLocal()
    item = UserHero(
            hero_id=hero_id,
            owner_id=user_id,
            incubated=incubated,
            in_team=in_team
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def get_token() -> str:
    return get_token_for(1)


def get_token_for(user_id: int) -> str:
    return create_token({"id": f"{user_id}", "sub": "User"})


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# getting team
def test_getting_team_without_authentication(test_db):
    response = client.get("/teams")
    assert response.status_code == 401


def test_getting_team_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/teams", headers=headers)
    assert response.status_code == 401


def test_getting_team_without_team_object(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/teams", headers=headers)
    assert response.status_code == 500


def test_getting_empty_team(test_db):
    user_id = create_user_and_return_id()
    create_team(user_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/teams", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert len(result['heroes']) == 0


def test_getting_team(test_db):
    user_id = create_user_and_return_id()
    team_id = create_team(user_id)
    add_to_team(
            team_id,
            create_user_hero(create_hero(1, "Hero 1"), user_id),
            1)
    add_to_team(
            team_id,
            create_user_hero(create_hero(2, "Hero 2"), user_id),
            2)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/teams", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert len(result['heroes']) == 2
    assert result['heroes'][0]['hero']['name'] == "Hero 1"
    assert result['heroes'][0]['hero']['id'] == 1
    assert result['heroes'][1]['hero']['name'] == "Hero 2"
    assert result['heroes'][1]['hero']['id'] == 2


# add hero
def test_adding_hero_without_authentication(test_db):
    response = client.post("/teams")
    assert response.status_code == 401


def test_adding_hero_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": 1,
                               "action": "add"
                               }
                           )
    assert response.status_code == 401


def test_adding_hero_without_hero_id(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "num": 1,
                               "action": "add"
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_without_num(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "action": "add"
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_without_action(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": 1,
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_with_negative_num(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": -1,
                               "action": "add"
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_with_num_zero(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": 0,
                               "action": "add"
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_with_num_greater_than_6(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": 7,
                               "action": "add"
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_without_team_initialized(test_db):
    user_id = create_user_and_return_id()
    hero_id = create_user_hero(create_hero(1, "Hero 1"), user_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": hero_id,
                               "num": 1,
                               "action": "add"
                               }
                           )
    assert response.status_code == 500


def test_adding_hero_without_hero(test_db):
    user_id = create_user_and_return_id()
    create_team(user_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": 1,
                               "action": "add"
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_with_incubated_hero(test_db):
    user_id = create_user_and_return_id()
    create_team(user_id)
    hero_id = create_user_hero(
            create_hero(1, "Hero 1"),
            user_id,
            incubated=True)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": hero_id,
                               "num": 1,
                               "action": "add"
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_with_hero_already_in_team(test_db):
    user_id = create_user_and_return_id()
    create_team(user_id)
    hero_id = create_user_hero(create_hero(1, "Hero 1"), user_id, in_team=True)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": hero_id,
                               "num": 1,
                               "action": "add"
                               }
                           )
    print(response.text)
    assert response.status_code == 400


def test_adding_hero(test_db):
    user_id = create_user_and_return_id()
    create_team(user_id)
    hero_id = create_user_hero(create_hero(1, "Hero 1"), user_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": hero_id,
                               "num": 1,
                               "action": "add"
                               }
                           )
    assert response.status_code == 200
    result = response.json()
    assert len(result['heroes']) == 1
    assert result['heroes'][0]['id'] == hero_id


def test_changing_added_hero_in_db(test_db):
    user_id = create_user_and_return_id()
    create_team(user_id)
    hero_id = create_user_hero(create_hero(1, "Hero 1"), user_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    client.post("/teams",
                headers=headers,
                json={
                    "hero_id": hero_id,
                    "num": 1,
                    "action": "add"
                    }
                )
    db = TestingSessionLocal()
    hero: UserHero = db.get(UserHero, hero_id)
    db.close()
    assert hero.in_team


def test_changing_old_hero_in_db_after_addition(test_db):
    user_id = create_user_and_return_id()
    team_id = create_team(user_id)
    hero_id = create_user_hero(create_hero(1, "Hero 1"), user_id)
    old_hero_id = create_user_hero(
            create_hero(2, "Hero 2"),
            user_id,
            in_team=True)
    add_to_team(team_id, old_hero_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    client.post("/teams",
                headers=headers,
                json={
                    "hero_id": hero_id,
                    "num": 1,
                    "action": "add"
                    }
                )
    db = TestingSessionLocal()
    hero: UserHero = db.get(UserHero, old_hero_id)
    db.close()
    assert not hero.in_team


def test_adding_hero_with_initial_gap(test_db):
    user_id = create_user_and_return_id()
    create_team(user_id)
    hero_id = create_user_hero(create_hero(1, "Hero 1"), user_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": hero_id,
                               "num": 2,
                               "action": "add"
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_with_gap_between_heroes(test_db):
    user_id = create_user_and_return_id()
    team_id = create_team(user_id)
    hero_id = create_user_hero(create_hero(1, "Hero 1"), user_id)
    old_hero_id = create_user_hero(
            create_hero(2, "Hero 2"),
            user_id,
            in_team=True)
    add_to_team(team_id, old_hero_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": hero_id,
                               "num": 3,
                               "action": "add"
                               }
                           )
    assert response.status_code == 400


def test_adding_hero_at_second_position(test_db):
    user_id = create_user_and_return_id()
    team_id = create_team(user_id)
    hero_id = create_user_hero(create_hero(1, "Hero 1"), user_id)
    old_hero_id = create_user_hero(
            create_hero(2, "Hero 2"),
            user_id,
            in_team=True)
    add_to_team(team_id, old_hero_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": hero_id,
                               "num": 2,
                               "action": "add"
                               }
                           )
    assert response.status_code == 200
    result = response.json()
    assert len(result['heroes']) == 2
    assert result['heroes'][0]['id'] == old_hero_id
    assert result['heroes'][1]['id'] == hero_id


# switching hero
def test_switching_hero_with_negative_switch_num(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": 1,
                               "switch_num": -1,
                               "action": "switch"
                               }
                           )
    assert response.status_code == 400


def test_switching_hero_with_zero_switch_num(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": 1,
                               "switch_num": 0,
                               "action": "switch"
                               }
                           )
    assert response.status_code == 400


def test_switching_hero_with_switch_num_greater_than_six(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": 1,
                               "switch_num": 7,
                               "action": "switch"
                               }
                           )
    assert response.status_code == 400


def test_switching_hero_without_switch_num(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/teams",
                           headers=headers,
                           json={
                               "hero_id": 1,
                               "num": 1,
                               "action": "switch"
                               }
                           )
    assert response.status_code == 400
