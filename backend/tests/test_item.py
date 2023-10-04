from fastapi.testclient import TestClient
import pytest
from timekeeper.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timekeeper.db.base import Base
from timekeeper.db.manager import get_db
from timekeeper.db.models import User, Item, ItemRarity, EquipmentEntry, ItemType
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


def create_item(id: int) -> int:
    db = TestingSessionLocal()
    item = Item(
            num=id,
            name=f"Item {id}",
            description="",
            rarity=ItemRarity.common,
            item_type=ItemType.crystal
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


def get_token() -> str:
    return get_token_for(1)


def get_token_for(user_id: int) -> str:
    return create_token({"id": f"{user_id}", "sub": "User"})


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# getting equipment
def test_getting_equipment_without_authentication(test_db):
    response = client.get("/items/")
    assert response.status_code == 401


def test_getting_equipment_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/items/",
                          headers=headers
                          )
    assert response.status_code == 401


def test_getting_users_items(test_db):
    id = create_user_and_return_id()
    create_equipment_item(create_item(1), id, 10)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/items/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]['item']['name'] == "Item 1"
    assert result[0]['amount'] == 10


def test_not_getting_other_users_items(test_db):
    id = create_user_and_return_id()
    other = create_user_with_username("User2")
    create_equipment_item(create_item(1), id, 10)
    create_equipment_item(create_item(2), other, 10)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/items/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]['item']['name'] == "Item 1"
    assert result[0]['amount'] == 10


def test_getting_first_page_of_items(test_db):
    id = create_user_and_return_id()
    for i in range(6):
        create_equipment_item(create_item(i), id, 10)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/items/?page=0&size=5",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 5


def test_getting_second_page_of_items(test_db):
    id = create_user_and_return_id()
    for i in range(6):
        create_equipment_item(create_item(i), id, 10)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/items/?page=1&size=5",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1


def test_getting_too_large_page_of_items(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/items/?page=0&size=125",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_negative_page_of_items(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/items/?page=-2&size=5",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_negative_amount_of_items(test_db):
    id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/items/?page=0&size=-5",
                          headers=headers
                          )
    assert response.status_code == 400


def test_getting_equipment_with_default_values(test_db):
    id = create_user_and_return_id()
    for i in range(0, 30):
        create_equipment_item(create_item(i), id, 10)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/items/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 20


def test_not_getting_empty_items(test_db):
    id = create_user_and_return_id()
    create_equipment_item(create_item(1), id, 0)
    create_equipment_item(create_item(2), id, 10)
    headers = {"Authorization": f"Bearer {get_token_for(id)}"}
    response = client.get("/items/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]['item']['name'] == "Item 2"
    assert result[0]['amount'] == 10
