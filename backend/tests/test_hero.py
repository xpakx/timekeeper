from fastapi.testclient import TestClient
import pytest
from timekeeper.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timekeeper.db.base import Base
from timekeeper.db.manager import get_db
from timekeeper.db.models import User, Item, ItemRarity, EquipmentEntry
from timekeeper.db.models import Hero, UserHero
from timekeeper.db.equipment_repo import CRYSTAL
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


def create_crystal() -> int:
    db = TestingSessionLocal()
    item = Item(
            num=CRYSTAL,
            name="Crystal",
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


def create_user_hero(hero_id: int, user_id: int):
    db = TestingSessionLocal()
    item = UserHero(
            hero_id=hero_id,
            owner_id=user_id,
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


# getting heroes
def test_getting_heroes_without_authentication(test_db):
    response = client.get("/heroes/")
    assert response.status_code == 401


def test_getting_heroes_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/heroes/",
                          headers=headers
                          )
    assert response.status_code == 401


def test_getting_users_heroes(test_db):
    id = create_user_and_return_id()
    create_user_hero(create_hero(1, "Hero"), id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/heroes/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]['hero']['name'] == "Hero"


def test_not_getting_other_users_heroes(test_db):
    id = create_user_and_return_id()
    other = create_user_with_username("User2")
    create_user_hero(create_hero(1, "Hero 1"), id)
    create_user_hero(create_hero(2, "Hero 2"), other)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/heroes/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]['hero']['name'] == "Hero 1"


def test_getting_first_page_of_heroes(test_db):
    id = create_user_and_return_id()
    for i in range(6):
        create_user_hero(create_hero(i, f"Hero {i}"), id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/heroes/?page=0&size=5",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 5


def test_getting_second_page_of_heroes(test_db):
    id = create_user_and_return_id()
    for i in range(6):
        create_user_hero(create_hero(i, f"Hero {i}"), id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/heroes/?page=1&size=5",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1


def test_getting_too_large_page_of_heroes(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/heroes/?page=0&size=125",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_negative_page_of_heroes(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/heroes/?page=-2&size=5",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_negative_amount_of_heroes(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/heroes/?page=0&size=-5",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_equipment_with_default_values(test_db):
    id = create_user_and_return_id()
    for i in range(0, 30):
        create_user_hero(create_hero(i, f"Hero {i}"), id)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/heroes/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 20


# getting crystals
def test_getting_crytals_without_authentication(test_db):
    response = client.get("/heroes/crystals")
    assert response.status_code == 401


def test_getting_crytals_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/heroes/crystals", headers=headers)
    assert response.status_code == 401


def test_getting_crytals_if_there_is_no_entry(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/heroes/crystals", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result['crystals'] == 0


def test_getting_crystals(test_db):
    user_id = create_user_and_return_id()
    create_equipment_item(create_crystal(), user_id, 12)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/heroes/crystals", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result['crystals'] == 12
