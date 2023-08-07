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
        Item,
        ItemRarity,
        EquipmentEntry,
        Incubator)
from timekeeper.db.models import Hero, UserHero
from timekeeper.services.incubator_service import INCUBATOR
from bcrypt import hashpw, gensalt
from timekeeper.services.user_service import create_token
from typing import Optional

NOT_INCUBATOR = 1

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


def create_item(id: int) -> int:
    db = TestingSessionLocal()
    item = Item(
            num=id,
            name="",
            description="",
            rarity=ItemRarity.uncommon
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_equipment_item(item_id: int, user_id: int, amount: int):
    db = TestingSessionLocal()
    item = EquipmentEntry(
            item_id=item_id,
            owner_id=user_id,
            amount=amount
            )
    db.add(item)
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


def create_user_hero(hero_id: int, user_id: int) -> int:
    db = TestingSessionLocal()
    item = UserHero(
            hero_id=hero_id,
            owner_id=user_id,
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_incubator(
        user_id: int,
        hero_id: Optional[int] = None,
        broken: bool = False):
    db = TestingSessionLocal()
    item = Incubator(
            hero_id=hero_id,
            owner_id=user_id,
            broken=broken,
            usages=5,
            permanent=False
            )
    db.add(item)
    db.commit()
    db.close()


def get_token() -> str:
    return get_token_for(1)


def get_token_for(user_id: int) -> str:
    return create_token({"id": f"{user_id}", "sub": "User"})


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# getting incubators
def test_getting_incubators_without_authentication(test_db):
    response = client.get("/incubators/")
    assert response.status_code == 401


def test_getting_incubators_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/incubators/",
                          headers=headers
                          )
    assert response.status_code == 401


def test_getting_users_incubators(test_db):
    id = create_user_and_return_id()
    create_incubator(id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/incubators/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1


def test_getting_users_incubators_with_hero(test_db):
    id = create_user_and_return_id()
    hero_id = create_user_hero(create_hero(1, "Hero"), id)
    create_incubator(id, hero_id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/incubators/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    print(result)
    assert result[0]['hero']['hero']['name'] == "Hero"


def test_not_getting_other_users_incubators(test_db):
    id = create_user_and_return_id()
    other = create_user_with_username("User2")
    create_incubator(id)
    create_incubator(other)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/incubators/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1


def test_not_getting_broken_incubators(test_db):
    id = create_user_and_return_id()
    create_incubator(id)
    create_incubator(id, broken=True)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/incubators/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1


# installing incubator
def test_installing_incubator_without_authentication(test_db):
    response = client.post("/incubators/")
    assert response.status_code == 401


def test_installing_incubator_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/incubators/",
                           headers=headers,
                           json={
                               "item_id": INCUBATOR
                               }
                           )
    assert response.status_code == 401


def test_installing_incubator_with_bad_item(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    create_equipment_item(create_item(NOT_INCUBATOR), id, 1)
    response = client.post("/incubators/",
                           headers=headers,
                           json={
                               "item_id": NOT_INCUBATOR
                               }
                           )
    assert response.status_code == 400


def test_installing_incubator_without_item_in_equipment(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    create_item(INCUBATOR)
    response = client.post("/incubators/",
                           headers=headers,
                           json={
                               "item_id": INCUBATOR
                               }
                           )
    assert response.status_code == 400


def test_installing_too_much_incubators(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    create_equipment_item(create_item(INCUBATOR), id, 1)
    for i in range(0, 5):
        create_incubator(id)
    response = client.post("/incubators/",
                           headers=headers,
                           json={
                               "item_id": INCUBATOR
                               }
                           )
    assert response.status_code == 400


def test_not_counting_broken_incubators_to_limit_while_installing_new_one(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    create_equipment_item(create_item(INCUBATOR), id, 1)
    for i in range(0, 4):
        create_incubator(id)
    create_incubator(id, broken=True)
    response = client.post("/incubators/",
                           headers=headers,
                           json={
                               "item_id": INCUBATOR
                               }
                           )
    assert response.status_code == 200
