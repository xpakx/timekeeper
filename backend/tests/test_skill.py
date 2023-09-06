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
        Hero,
        UserHero,
        ItemRarity,
        EquipmentEntry,
        ItemType,
        SkillHero,
        Skill,
        SkillSet)
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


def create_skillset(hero_id: int):
    db = TestingSessionLocal()
    entry = SkillSet(
            hero_id=hero_id,
            usages_1=0,
            usages_2=0,
            usages_3=0,
            usages_4=0
            )
    db.add(entry)
    db.commit()
    db.close()


def create_user_and_return_id() -> int:
    return create_user_with_username("User")


def create_item(id: int, skill: bool = False) -> int:
    db = TestingSessionLocal()
    item = Item(
            num=id,
            name=f"Item {id}",
            description="",
            rarity=ItemRarity.common,
            item_type=ItemType.skill if skill else ItemType.crystal
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
            incubated=False
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_skill(item_id: int) -> int:
    db = TestingSessionLocal()
    skill = Skill(
            item_id=item_id,
            )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    db.close()
    return skill.id


def make_skill_teachable_for(skill_id: int, hero_id: int):
    db = TestingSessionLocal()
    hero_skill = SkillHero(
            skill_id=skill_id,
            hero_id=hero_id
            )
    db.add(hero_skill)
    db.commit()
    db.close()


def get_token() -> str:
    return get_token_for(1)


def get_token_for(user_id: int) -> str:
    return create_token({"id": f"{user_id}", "sub": "User"})


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# getting heroes
def test_teaching_skill_without_authentication(test_db):
    response = client.post("/heroes/1/skills")
    assert response.status_code == 401


def test_teaching_skill_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/heroes/1/skills",
                           headers=headers,
                           json={
                               "item_id": 1,
                               "num": 1
                               }
                           )
    assert response.status_code == 401


def test_teaching_skill_without_item(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               "item_id": 1,
                               "num": 1
                               }
                           )
    assert response.status_code == 400


def test_teaching_skill_with_zero_items(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    create_equipment_item(create_item(10), user_id, 0)
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               "item_id": 10,
                               "num": 1
                               }
                           )
    assert response.status_code == 400


def test_teaching_skill_with_non_skill_item(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    item_id = create_item(10, skill=False)
    create_equipment_item(item_id, user_id, 1)
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               "item_id": 10,
                               "num": 1
                               }
                           )
    assert response.status_code == 400


def test_teaching_skill_with_no_hero(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    item_id = create_item(10, skill=True)
    create_equipment_item(item_id, user_id, 1)
    response = client.post("/heroes/1/skills",
                           headers=headers,
                           json={
                               "item_id": 10,
                               "num": 1
                               }
                           )
    assert response.status_code == 404


def test_teaching_skill_to_hero(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    create_skillset(hero_id)
    item_id = create_item(10, skill=True)
    skill_id = create_skill(item_id)
    make_skill_teachable_for(skill_id, hero_id)
    create_equipment_item(item_id, user_id, 1)
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               "item_id": 10,
                               "num": 1
                               }
                           )
    assert response.status_code == 200


def test_teaching_skill_while_no_skill_found(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    create_skillset(hero_id)
    item_id = create_item(10, skill=True)
    create_equipment_item(item_id, user_id, 1)
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               "item_id": 10,
                               "num": 1
                               }
                           )
    print(response.text)
    assert response.status_code == 500


def test_teaching_non_teachable_skill(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    create_skillset(hero_id)
    item_id = create_item(10, skill=True)
    create_skill(item_id)
    create_equipment_item(item_id, user_id, 1)
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               "item_id": 10,
                               "num": 1
                               }
                           )
    assert response.status_code == 400


def test_teaching_skill_without_skillset(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    item_id = create_item(10, skill=True)
    skill_id = create_skill(item_id)
    make_skill_teachable_for(skill_id, hero_id)
    create_equipment_item(item_id, user_id, 1)
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               "item_id": 10,
                               "num": 1
                               }
                           )
    assert response.status_code == 500
