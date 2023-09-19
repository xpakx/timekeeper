from timekeeper.db.models import (
        ExpGroup,
        UserHero,
        Hero,
        User,
        Battle,
        HeroMods,
        HeroType,
        Item,
        SkillSet,
        EquipmentEntry,
        ItemType,
        ItemRarity,
        Team)
from fastapi.testclient import TestClient
import pytest
from timekeeper.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timekeeper.db.base import Base
from timekeeper.db.manager import get_db
from bcrypt import hashpw, gensalt
from timekeeper.services.user_service import create_token
from unittest.mock import patch, Mock

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
ITEM_NUM = 123


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


def create_bulbasaur() -> int:
    db = TestingSessionLocal()
    item = Hero(
            num=1,
            name="Bulbasaur",
            title="Seed Pokemon",
            rarity=ItemRarity.uncommon,
            hero_type=HeroType.grass,
            secondary_hero_type=HeroType.poison,
            base_hp=45,
            base_attack=49,
            base_defense=49,
            base_speed=45,
            base_special_attack=65,
            base_special_defense=65,
            exp_group=ExpGroup.medium_slow
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_charmander() -> int:
    db = TestingSessionLocal()
    item = Hero(
            num=4,
            name="Charmander",
            title="Lizard Pokemon",
            rarity=ItemRarity.uncommon,
            hero_type=HeroType.fire,
            base_hp=39,
            base_attack=52,
            base_defense=43,
            base_speed=65,
            base_special_attack=60,
            base_special_defense=50,
            exp_group=ExpGroup.medium_slow
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
            incubated=False,
            hp=0,
            attack=0,
            defense=0,
            speed=0,
            special_attack=0,
            special_defense=0,
            level=1,
            damage=0
            )
    entry = SkillSet(
            hero=item,
            usages_1=0,
            usages_2=0,
            usages_3=0,
            usages_4=0
            )
    db.add(item)
    db.add(entry)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_battle(
        user_id: int,
        hero_id: int,
        enemy_id: int,
        finished: bool = False):
    db = TestingSessionLocal()
    hero = HeroMods(
            accuracy=0,
            evasion=0,
            attack=0,
            defense=0,
            special_attack=0,
            special_defense=0,
            speed=0)
    enemy = HeroMods(
            accuracy=0,
            evasion=0,
            attack=0,
            defense=0,
            special_attack=0,
            special_defense=0,
            speed=0)
    item = Battle(
            turn=1,
            enemies=1,
            finished=finished,
            hero_id=hero_id,
            hero_mods=hero,
            enemy_id=enemy_id,
            enemy_mods=enemy,
            owner_id=user_id
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_battle_ticket(wrong_type: bool = False) -> int:
    db = TestingSessionLocal()
    item = Item(
            num=ITEM_NUM,
            name="Battle Ticket",
            description="",
            rarity=ItemRarity.uncommon,
            item_type=ItemType.battle_ticket if not wrong_type else ItemType.skill
            )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item.id


def create_equipment_item(item_id: int, user_id: int, amount: int = 1):
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


def get_token() -> str:
    return get_token_for(1)


def get_token_for(user_id: int) -> str:
    return create_token({"id": f"{user_id}", "sub": "User"})


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# getting current battle
def test_getting_current_battle_without_authentication(test_db):
    response = client.get("/battles/")
    assert response.status_code == 401


def test_getting_current_battle_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/battles/",
                          headers=headers
                          )
    assert response.status_code == 401


def test_getting_current_battle_while_no_battles(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/battles/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert result is None


def test_getting_current_battle_while_no_unfinished_battle(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    enemy_id = create_user_hero(create_charmander(), None)
    create_battle(user_id, hero_id, enemy_id, finished=True)
    response = client.get("/battles/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert result is None


def test_getting_current_battle(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    enemy_id = create_user_hero(create_charmander(), None)
    battle_id = create_battle(user_id, hero_id, enemy_id, finished=False)
    response = client.get("/battles/",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert result['id'] == battle_id


# getting battle
def test_getting_battle_without_authentication(test_db):
    response = client.get("/battles/1")
    assert response.status_code == 401


def test_getting_battle_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.get("/battles/1",
                          headers=headers
                          )
    assert response.status_code == 401


def test_getting_battle_while_not_found(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    response = client.get("/battles/1",
                          headers=headers
                          )
    assert response.status_code == 404
    error = response.json()
    assert "battle" in error['detail'].lower()
    assert "not found" in error['detail']


def test_getting_battle(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    enemy_id = create_user_hero(create_charmander(), None)
    battle_id = create_battle(user_id, hero_id, enemy_id)
    response = client.get(f"/battles/{battle_id}",
                          headers=headers
                          )
    assert response.status_code == 200
    result = response.json()
    assert result['id'] == battle_id


# starting battle
def test_starting_battle_without_authentication(test_db):
    response = client.post("/battles")
    assert response.status_code == 401


def test_starting_battle_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/battles",
                           headers=headers
                           )
    assert response.status_code == 401


def test_starting_battle_while_already_in_battle(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    enemy_id = create_user_hero(create_charmander(), None)
    create_battle(user_id, hero_id, enemy_id)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": 1,
                               }
                           )
    assert response.status_code == 400
    error = response.json()
    assert "in battle" in error['detail']


def test_starting_battle_without_battle_ticket_item(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": 1,
                               }
                           )
    assert response.status_code == 400
    error = response.json()
    assert "no battle ticket" in error['detail'].lower()


def test_starting_battle_with_zero_battle_tickets(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    create_equipment_item(create_battle_ticket(), user_id, 0)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 400
    error = response.json()
    assert "battle ticket" in error['detail']
    assert "not enough" in error['detail'].lower()


def test_starting_battle_with_battle_ticket_with_wrong_item_type(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    create_equipment_item(create_battle_ticket(wrong_type=True), user_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 400
    error = response.json()
    assert "no battle ticket" in error['detail'].lower()


def test_starting_battle_with_not_team_initialized(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    create_equipment_item(create_battle_ticket(), user_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 500
    error = response.json()
    assert "team" in error['detail'].lower()
    assert "initialized" in error['detail'].lower()


def test_starting_battle_with_empty_team(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    create_user_hero(create_bulbasaur(), user_id)
    create_team(user_id)
    create_equipment_item(create_battle_ticket(), user_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 400
    error = response.json()
    assert "team" in error['detail'].lower()
    assert "empty" in error['detail'].lower()


@patch('random.choice', Mock(return_value=4))
def test_starting_battle_without_heroes_initialized(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    create_equipment_item(create_battle_ticket(), user_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 500
    error = response.json()
    assert "heroes" in error['detail'].lower()
    print(response.text)
    assert "initialized" in error['detail'].lower()


@patch('random.choice', Mock(return_value=4))
def test_starting_battle(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    create_charmander()
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    create_equipment_item(create_battle_ticket(), user_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 200


@patch('random.choice', Mock(return_value=4))
def test_subtracting_battle_ticket_while_starting_battle(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    create_charmander()
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    item_id = create_equipment_item(create_battle_ticket(), user_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 200
    db = TestingSessionLocal()
    item = db.query(EquipmentEntry).where(EquipmentEntry.id == item_id).first()
    db.close()
    assert item is not None
    assert item.amount == 0


@patch('random.choice', Mock(return_value=4))
def test_creating_battle_in_db(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    create_charmander()
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    create_equipment_item(create_battle_ticket(), user_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 200
    battle_id = response.json()['id']
    db = TestingSessionLocal()
    battle: Battle = db.query(Battle).where(Battle.id == battle_id).first()
    db.close()
    assert battle is not None
    assert battle.hero_id == hero_id


@patch('random.choice', Mock(return_value=4))
def test_saving_mods_while_creating_battle(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    create_charmander()
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    create_equipment_item(create_battle_ticket(), user_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 200
    battle_id = response.json()['id']
    db = TestingSessionLocal()
    battle: Battle = db.query(Battle).where(Battle.id == battle_id).first()
    db.close()
    assert battle.hero_mods_id is not None
    assert battle.enemy_mods_id is not None
    assert battle.enemy_id is not None


@patch('random.choice', Mock(return_value=4))
def test_saving_enemy_while_creating_battle(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    char_id = create_charmander()
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    team_id = create_team(user_id)
    add_to_team(team_id, hero_id, 1)
    create_equipment_item(create_battle_ticket(), user_id, 1)
    response = client.post("/battles",
                           headers=headers,
                           json={
                               "id": ITEM_NUM,
                               }
                           )
    assert response.status_code == 200
    battle_id = response.json()['id']
    db = TestingSessionLocal()
    battle: Battle = db.query(Battle).where(Battle.id == battle_id).first()
    enemy_id = battle.enemy.hero.id
    db.close()
    assert battle.enemy_id is not None
    assert enemy_id == char_id


# starting battle
def test_making_move_without_authentication(test_db):
    response = client.post("/battles/1")
    assert response.status_code == 401


def test_making_move_with_wrong_token(test_db):
    headers = {"Authorization": "Bearer wrong_token"}
    response = client.post("/battles/1",
                           headers=headers
                           )
    assert response.status_code == 401


def test_fleeing(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    enemy_id = create_user_hero(create_charmander(), None)
    battle_id = create_battle(user_id, hero_id, enemy_id)
    response = client.post(f"/battles/{battle_id}",
                           headers=headers,
                           json={
                               'move': 'flee'
                               }
                           )
    assert response.status_code == 200


def test_advancing_turns(test_db):
    user_id = create_user_and_return_id()
    headers = {"Authorization": f"Bearer {get_token_for(user_id)}"}
    hero_id = create_user_hero(create_bulbasaur(), user_id)
    enemy_id = create_user_hero(create_charmander(), None)
    battle_id = create_battle(user_id, hero_id, enemy_id)
    client.post(f"/battles/{battle_id}",
                headers=headers,
                json={
                    'move': 'flee'
                    }
                )
    db = TestingSessionLocal()
    battle = db.query(Battle).where(Battle.id == battle_id).first()
    db.close()
    assert battle is not None
    assert battle.turn == 2
