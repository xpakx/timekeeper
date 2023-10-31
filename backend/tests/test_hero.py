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
        ItemType,
        SkillSet,
        Skill,
        SkillHero,
        HeroEvolve)
from timekeeper.db.models import Hero, UserHero
from bcrypt import hashpw, gensalt
from timekeeper.services.user_service import create_token
from typing import Optional

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
ITEM_ID = 4
CRYSTAL = 6


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


def teach_skill(hero_id: int, skill_id: int, num: int = 1):
    db = TestingSessionLocal()
    skillset: SkillSet = db\
        .query(SkillSet)\
        .where(SkillSet.hero_id == hero_id)\
        .first()
    if num == 1:
        skillset.skill_1_id = skill_id
    if num == 2:
        skillset.skill_2_id = skill_id
    if num == 3:
        skillset.skill_3_id = skill_id
    if num == 4:
        skillset.skill_4_id = skill_id
    db.commit()
    db.close()


def create_skill(item_id: Optional[int]) -> int:
    db = TestingSessionLocal()
    skill = Skill(
            power=100,
            priority=0,
            item_id=item_id
            )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    db.close()
    return skill.id


def make_teachable(skill_id: int, hero_id: int) -> int:
    db = TestingSessionLocal()
    skill = SkillHero(
            skill_id=skill_id,
            hero_id=hero_id,
            )
    db.add(skill)
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
            rarity=ItemRarity.uncommon,
            item_type=ItemType.crystal
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_item(skill_type: bool = True) -> int:
    db = TestingSessionLocal()
    item = Item(
            num=ITEM_ID,
            name="Skill",
            description="",
            rarity=ItemRarity.uncommon,
            item_type=ItemType.skill if skill_type else ItemType.crystal
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_equipment_item(item_id: int, user_id: int, amount: int) -> int:
    db = TestingSessionLocal()
    item = EquipmentEntry(
            item_id=item_id,
            owner_id=user_id,
            amount=amount
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


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


def create_user_hero(hero_id: int, user_id: int, skillset: bool = False, level: int = 1) -> int:
    db = TestingSessionLocal()
    item = UserHero(
            hero_id=hero_id,
            owner_id=user_id,
            incubated=False,
            level=level
            )
    db.add(item)
    if skillset:
        entry = SkillSet(
                hero=item,
                usages_1=0,
                usages_2=0,
                usages_3=0,
                usages_4=0
                )
        db.add(entry)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_hero_(id: int, db):
    item = Hero(
            num=id,
            name=f"Hero {id}",
            description="",
            rarity=ItemRarity.uncommon
            )
    db.add(item)


def create_heroes():
    db = TestingSessionLocal()
    for i in range(1, 21):
        create_hero_(i, db)
    db.commit()
    db.close()


def add_evolved_form(hero_id: int, evolved_id: int, level: int) -> None:
    db = TestingSessionLocal()
    item = HeroEvolve(
            hero_id=hero_id,
            evolve_id=evolved_id,
            min_level=level
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


# hero randomization

def test_getting_hero_without_authentication(test_db):
    response = client.get("/heroes/reward")
    assert response.status_code == 401


def test_getting_hero_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/heroes/reward", headers=headers)
    assert response.status_code == 401


def test_getting_hero_if_no_crystals(test_db):
    create_heroes()
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/heroes/reward", headers=headers)
    assert response.status_code == 400


def test_getting_hero(test_db):
    create_heroes()
    user_id = create_user_and_return_id()
    create_equipment_item(create_crystal(), user_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/heroes/reward", headers=headers)
    assert response.status_code == 200


def test_getting_hero_without_data_in_db(test_db):
    user_id = create_user_and_return_id()
    create_equipment_item(create_crystal(), user_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/heroes/reward", headers=headers)
    assert response.status_code == 500


# skill teaching
def test_teaching_hero_skill_without_authentication(test_db):
    response = client.post("/heroes/1/skills")
    assert response.status_code == 401


def test_teaching_hero_skill_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/heroes/1/skills",
                           json={
                               'item_id': 1,
                               'num': 1
                               },
                           headers=headers)
    assert response.status_code == 401


def test_teaching_skill_without_num(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/heroes/1/skills",
                           headers=headers,
                           json={
                               'item_id': 1,
                               },
                           )
    assert response.status_code == 400


def test_teaching_skill_with_negative_num(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/heroes/1/skills",
                           headers=headers,
                           json={
                               'item_id': 1,
                               'num': -1
                               },
                           )
    assert response.status_code == 400


def test_teaching_skill_with_zero_num(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/heroes/1/skills",
                           headers=headers,
                           json={
                               'item_id': 1,
                               'num': 0
                               },
                           )
    assert response.status_code == 400


def test_teaching_skill_with_num_higher_than_4(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/heroes/1/skills",
                           headers=headers,
                           json={
                               'item_id': 1,
                               'num': 5
                               },
                           )
    assert response.status_code == 400


def test_teaching_skill_without_item_id(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/heroes/1/skills",
                           headers=headers,
                           json={
                               'num': 1,
                               },
                           )
    assert response.status_code == 400


def test_teaching_skill_without_item(test_db):
    user_id = create_user_and_return_id()
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               'num': 1,
                               'item_id': 1
                               },
                           )
    assert response.status_code == 400
    error = response.json()
    print(error)
    assert "no item" in error['detail'].lower()


def test_teaching_skill_with_zero_item_count(test_db):
    user_id = create_user_and_return_id()
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    create_equipment_item(create_item(), user_id, 0)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               'num': 1,
                               'item_id': ITEM_ID
                               },
                           )
    assert response.status_code == 400
    error = response.json()
    print(error)
    assert "no item" in error['detail'].lower()


def test_teaching_skill_to_nonexistent_hero(test_db):
    user_id = create_user_and_return_id()
    create_equipment_item(create_item(), user_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post("/heroes/1/skills",
                           headers=headers,
                           json={
                               'num': 1,
                               'item_id': ITEM_ID
                               },
                           )
    assert response.status_code == 404
    error = response.json()
    assert "not" in error['detail'].lower()
    assert "hero" in error['detail'].lower()


def test_teaching_skill(test_db):
    user_id = create_user_and_return_id()
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id, skillset=True)
    item_id = create_item()
    skill_id = create_skill(item_id)
    make_teachable(skill_id, hero_id)
    create_equipment_item(item_id, user_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               'num': 1,
                               'item_id': ITEM_ID
                               },
                           )
    assert response.status_code == 200


def test_teaching_skill_withou_skillset_initialized(test_db):
    user_id = create_user_and_return_id()
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id)
    item_id = create_item()
    skill_id = create_skill(item_id)
    make_teachable(skill_id, hero_id)
    create_equipment_item(item_id, user_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               'num': 1,
                               'item_id': ITEM_ID
                               },
                           )
    assert response.status_code == 500
    error = response.json()
    assert "skillset" in error['detail'].lower()
    assert "initialized" in error['detail'].lower()


def test_teaching_nonteachable_skill(test_db):
    user_id = create_user_and_return_id()
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id, skillset=True)
    item_id = create_item()
    create_skill(item_id)
    create_equipment_item(item_id, user_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               'num': 1,
                               'item_id': ITEM_ID
                               },
                           )
    assert response.status_code == 400
    error = response.json()
    assert "teachable" in error['detail'].lower()


def test_teaching_non_initialized_skill(test_db):
    user_id = create_user_and_return_id()
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id, skillset=True)
    item_id = create_item()
    create_equipment_item(item_id, user_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               'num': 1,
                               'item_id': ITEM_ID
                               },
                           )
    assert response.status_code == 500
    error = response.json()
    assert "skill" in error['detail'].lower()
    assert "initialized" in error['detail'].lower()


def test_teaching_skill_at_already_taken_postion(test_db):
    user_id = create_user_and_return_id()
    hero_id = create_user_hero(create_hero(1, 'Hero'), user_id, skillset=True)
    item_id = create_item()
    skill_id = create_skill(item_id)
    second_skill = create_skill(None)
    teach_skill(hero_id, second_skill, 1)
    make_teachable(skill_id, hero_id)
    create_equipment_item(item_id, user_id, 1)
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.post(f"/heroes/{hero_id}/skills",
                           headers=headers,
                           json={
                               'num': 1,
                               'item_id': ITEM_ID
                               },
                           )
    assert response.status_code == 200


# evolving hero
def test_evolving_hero_without_authentication(test_db):
    response = client.post("/heroes/1/evolve")
    assert response.status_code == 401


def test_evolving_hero_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/heroes/1/evolve",
                           headers=headers,
                           json={
                               'hero_id': 2
                               },
                           )
    assert response.status_code == 401


def test_evolving_hero_if_no_next_form(test_db):
    create_heroes()
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_hero(1, 'Hero')
    next_id = create_hero(2, 'New Hero')
    user_hero_id = create_user_hero(hero_id, user_id, skillset=True)
    response = client.post(f"/heroes/{user_hero_id}/evolve",
                           headers=headers,
                           json={
                               'hero_id': next_id
                               },
                           )
    assert response.status_code == 400


def test_evolving_hero_if_nonexistent_next_form(test_db):
    create_heroes()
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_hero(1, 'Hero')
    user_hero_id = create_user_hero(hero_id, user_id, skillset=True)
    response = client.post(f"/heroes/{user_hero_id}/evolve",
                           headers=headers,
                           json={
                               'hero_id': 1
                               },
                           )
    assert response.status_code == 400


def test_evolving_hero_if_no_hero(test_db):
    create_heroes()
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    next_id = create_hero(2, 'New Hero')
    response = client.post("/heroes/1/evolve",
                           headers=headers,
                           json={
                               'hero_id': next_id
                               },
                           )
    assert response.status_code == 404


def test_evolving_hero_if_wrong_level(test_db):
    create_heroes()
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_hero(1, 'Hero')
    next_id = create_hero(2, 'New Hero')
    add_evolved_form(hero_id, next_id, 10)
    user_hero_id = create_user_hero(hero_id, user_id, skillset=True, level=9)
    response = client.post(f"/heroes/{user_hero_id}/evolve",
                           headers=headers,
                           json={
                               'hero_id': next_id
                               },
                           )
    assert response.status_code == 400


def test_evolving_hero(test_db):
    create_heroes()
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_hero(1, 'Hero')
    next_id = create_hero(2, 'New Hero')
    add_evolved_form(hero_id, next_id, 10)
    user_hero_id = create_user_hero(hero_id, user_id, skillset=True, level=10)
    response = client.post(f"/heroes/{user_hero_id}/evolve",
                           headers=headers,
                           json={
                               'hero_id': next_id
                               },
                           )
    assert response.status_code == 200


def test_evolving_hero_with_higher_level(test_db):
    create_heroes()
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_hero(1, 'Hero')
    next_id = create_hero(2, 'New Hero')
    add_evolved_form(hero_id, next_id, 10)
    user_hero_id = create_user_hero(hero_id, user_id, skillset=True, level=15)
    response = client.post(f"/heroes/{user_hero_id}/evolve",
                           headers=headers,
                           json={
                               'hero_id': next_id
                               },
                           )
    assert response.status_code == 200
